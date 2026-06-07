#!/usr/bin/env python3
"""Minimal SAP AI Core foundation-model client for V30.

Credentials are read from SAP_AI_CORE_API_KEY in .env/environment. The value is
expected to be an SAP service-key JSON object or a base64-encoded JSON object.
No client secret, service-key JSON, or bearer token is printed.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_RESOURCE_GROUP = "default"


class SapAiCoreError(RuntimeError):
    pass


def load_dotenv(path: str = ".env") -> None:
    env_path = pathlib.Path(path)
    if not env_path.exists():
        return
    for raw in env_path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _json_from_env_value(value: str) -> dict[str, Any]:
    value = value.strip()
    if not value:
        raise SapAiCoreError("SAP_AI_CORE_API_KEY is empty")
    if pathlib.Path(value).exists():
        value = pathlib.Path(value).read_text()
    try:
        obj = json.loads(value)
    except json.JSONDecodeError:
        try:
            obj = json.loads(base64.b64decode(value).decode("utf-8"))
        except Exception as exc:
            raise SapAiCoreError(
                "SAP_AI_CORE_API_KEY is neither JSON service-key nor base64 JSON"
            ) from exc
    if not isinstance(obj, dict):
        raise SapAiCoreError("SAP_AI_CORE_API_KEY decoded to non-object JSON")
    return obj


def credential() -> dict[str, Any]:
    load_dotenv()
    raw = os.environ.get("SAP_AI_CORE_API_KEY", "")
    cred = _json_from_env_value(raw)
    required = ["clientid", "clientsecret", "url", "serviceurls"]
    missing = [key for key in required if key not in cred]
    if missing:
        raise SapAiCoreError(f"SAP service key missing required keys: {missing}")
    if "AI_API_URL" not in cred.get("serviceurls", {}):
        raise SapAiCoreError("SAP service key missing serviceurls.AI_API_URL")
    return cred


def host(url: str) -> str:
    match = re.match(r"https?://([^/]+)", url)
    return match.group(1) if match else ""


def oauth_token(cred: dict[str, Any]) -> tuple[str, int | None]:
    token_url = cred["url"].rstrip("/") + "/oauth/token"
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(token_url, data=data, method="POST")
    basic = base64.b64encode(
        f"{cred['clientid']}:{cred['clientsecret']}".encode()
    ).decode()
    req.add_header("Authorization", f"Basic {basic}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload["access_token"], payload.get("expires_in")


def request_json(
    url: str,
    token: str,
    resource_group: str,
    method: str = "GET",
    body: dict[str, Any] | None = None,
    timeout: int = 60,
) -> tuple[int, dict[str, Any]]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("AI-Resource-Group", resource_group)
    if body is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="ignore")
        try:
            detail = json.loads(raw)
        except Exception:
            detail = {"raw": raw}
        raise SapAiCoreError(f"HTTP {exc.code} from {url}: {detail}") from exc


def deployments(
    cred: dict[str, Any], token: str, resource_group: str
) -> list[dict[str, Any]]:
    url = cred["serviceurls"]["AI_API_URL"].rstrip("/") + "/v2/lm/deployments"
    _, payload = request_json(url, token, resource_group)
    return payload.get("resources", [])


def model_info(resource: dict[str, Any]) -> dict[str, str]:
    details = resource.get("details", {})
    model = (
        details.get("resources", {}).get("backendDetails", {}).get("model")
        or details.get("resources", {}).get("backend_details", {}).get("model")
        or details.get("backendDetails", {}).get("model")
        or details.get("backend_details", {}).get("model")
        or {}
    )
    return {
        "id": resource.get("id", ""),
        "name": model.get("name", ""),
        "version": model.get("version", ""),
        "status": resource.get("status", ""),
        "deploymentUrl": resource.get("deploymentUrl", "")
        or resource.get("deployment_url", ""),
    }


def find_deployment(resources: list[dict[str, Any]], model_query: str) -> dict[str, str]:
    infos = [model_info(item) for item in resources]
    exact = [item for item in infos if item["name"] == model_query]
    if exact:
        return exact[0]
    partial = [item for item in infos if model_query.lower() in item["name"].lower()]
    if partial:
        return partial[0]
    raise SapAiCoreError(f"No deployment found for model query: {model_query}")


def gemini_generate(
    deployment: dict[str, str],
    token: str,
    resource_group: str,
    prompt: str,
    timeout: int,
    max_output_tokens: int,
) -> str:
    model = deployment["name"]
    url = deployment["deploymentUrl"].rstrip("/") + f"/models/{model}:generateContent"
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_output_tokens, "temperature": 0.2},
    }
    _, payload = request_json(url, token, resource_group, "POST", body, timeout)
    try:
        return payload["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as exc:
        raise SapAiCoreError(f"Unexpected Gemini response schema: {payload}") from exc


def chat_completions_generate(
    deployment: dict[str, str],
    token: str,
    resource_group: str,
    prompt: str,
    timeout: int,
    max_output_tokens: int,
) -> str:
    model = deployment["name"]
    url = deployment["deploymentUrl"].rstrip("/") + "/chat/completions"
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_output_tokens,
        "temperature": 0.2,
    }
    _, payload = request_json(url, token, resource_group, "POST", body, timeout)
    try:
        return payload["choices"][0]["message"]["content"]
    except Exception as exc:
        raise SapAiCoreError(f"Unexpected chat-completions response schema: {payload}") from exc


def generate(
    deployment: dict[str, str],
    token: str,
    resource_group: str,
    prompt: str,
    timeout: int,
    max_output_tokens: int,
) -> str:
    name = deployment["name"]
    if name.startswith("gemini"):
        return gemini_generate(
            deployment, token, resource_group, prompt, timeout, max_output_tokens
        )
    if name.startswith("mistralai") or name.startswith("gpt-"):
        return chat_completions_generate(
            deployment, token, resource_group, prompt, timeout, max_output_tokens
        )
    if name.startswith("anthropic"):
        raise SapAiCoreError(
            "Anthropic deployment discovered, but no allowed native subpath was "
            "identified in V30 probes. Tested /completion, /chat/completions, "
            "/messages, /v1/messages, root, and model/invoke variants."
        )
    raise SapAiCoreError(f"No implemented request schema for model: {name}")


def cmd_inspect(_: argparse.Namespace) -> int:
    cred = credential()
    print("credential_format: json service key")
    print("auth_host:", host(cred["url"]))
    print("ai_api_host:", host(cred["serviceurls"]["AI_API_URL"]))
    print("top_level_keys:", ",".join(sorted(cred.keys())))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    cred = credential()
    token, expires = oauth_token(cred)
    print("oauth: ok; expires_in:", expires)
    resources = deployments(cred, token, args.resource_group)
    print("deployment_count:", len(resources))
    for item in resources:
        info = model_info(item)
        print(
            "\t".join(
                [
                    info["id"],
                    info["status"],
                    info["name"],
                    info["version"],
                    info["deploymentUrl"],
                ]
            )
        )
    return 0


def cmd_smoke(args: argparse.Namespace) -> int:
    cred = credential()
    token, expires = oauth_token(cred)
    resources = deployments(cred, token, args.resource_group)
    deployment = find_deployment(resources, args.model)
    started = time.time()
    text = generate(
        deployment,
        token,
        args.resource_group,
        "Reply with exactly OK.",
        args.timeout,
        args.max_output_tokens,
    )
    elapsed = time.time() - started
    print("oauth: ok; expires_in:", expires)
    print("model:", deployment["name"], deployment["version"], deployment["id"])
    print("smoke_elapsed_sec:", round(elapsed, 2))
    print("response:", text.strip()[:200])
    return 0


def cmd_prompt(args: argparse.Namespace) -> int:
    cred = credential()
    token, _ = oauth_token(cred)
    resources = deployments(cred, token, args.resource_group)
    deployment = find_deployment(resources, args.model)
    prompt = args.prompt
    if args.prompt_file:
        prompt = pathlib.Path(args.prompt_file).read_text()
    text = generate(
        deployment,
        token,
        args.resource_group,
        prompt,
        args.timeout,
        args.max_output_tokens,
    )
    if args.output:
        pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(args.output).write_text(text)
    else:
        print(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_parser = sub.add_parser("inspect", help="Inspect credential shape safely")
    inspect_parser.set_defaults(func=cmd_inspect)

    list_parser = sub.add_parser("list-deployments", help="List model deployments")
    list_parser.add_argument("--resource-group", default=os.getenv("SAP_AI_CORE_RESOURCE_GROUP", DEFAULT_RESOURCE_GROUP))
    list_parser.set_defaults(func=cmd_list)

    smoke_parser = sub.add_parser("smoke", help="Run a one-prompt model smoke test")
    smoke_parser.add_argument("--model", required=True, help="Exact or partial model name")
    smoke_parser.add_argument("--resource-group", default=os.getenv("SAP_AI_CORE_RESOURCE_GROUP", DEFAULT_RESOURCE_GROUP))
    smoke_parser.add_argument("--timeout", type=int, default=60)
    smoke_parser.add_argument("--max-output-tokens", type=int, default=64)
    smoke_parser.set_defaults(func=cmd_smoke)

    prompt_parser = sub.add_parser("prompt", help="Send a prompt to a model")
    prompt_parser.add_argument("--model", required=True, help="Exact or partial model name")
    prompt_parser.add_argument("--prompt", default="")
    prompt_parser.add_argument("--prompt-file")
    prompt_parser.add_argument("--output")
    prompt_parser.add_argument("--resource-group", default=os.getenv("SAP_AI_CORE_RESOURCE_GROUP", DEFAULT_RESOURCE_GROUP))
    prompt_parser.add_argument("--timeout", type=int, default=120)
    prompt_parser.add_argument("--max-output-tokens", type=int, default=8192)
    prompt_parser.set_defaults(func=cmd_prompt)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except SapAiCoreError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
