// Stream a coordinate Matrix Market file from stdin and retain only frozen
// target-gene counts plus full-library totals for selected cell columns.

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

class FastUnsignedReader {
 public:
  bool next(std::uint32_t& value) {
    int c = read_char();
    while (c != EOF && (c < '0' || c > '9')) {
      c = read_char();
    }
    if (c == EOF) {
      return false;
    }
    std::uint32_t parsed = 0;
    do {
      parsed = parsed * 10U + static_cast<std::uint32_t>(c - '0');
      c = read_char();
    } while (c >= '0' && c <= '9');
    value = parsed;
    return true;
  }

 private:
  static constexpr std::size_t kBufferSize = 1U << 20U;
  char buffer_[kBufferSize];
  std::size_t position_ = 0;
  std::size_t length_ = 0;

  int read_char() {
    if (position_ == length_) {
      length_ = std::fread(buffer_, 1, kBufferSize, stdin);
      position_ = 0;
      if (length_ == 0) {
        return EOF;
      }
    }
    return static_cast<unsigned char>(buffer_[position_++]);
  }
};

struct Target {
  std::uint32_t row = 0;
  std::string gene;
};

[[noreturn]] void fail(const std::string& message) {
  std::cerr << "ERROR: " << message << '\n';
  std::exit(2);
}

std::vector<Target> read_targets(const std::string& path) {
  std::ifstream input(path);
  if (!input) {
    fail("cannot open target-row file: " + path);
  }
  std::string line;
  std::getline(input, line);
  std::vector<Target> targets;
  while (std::getline(input, line)) {
    if (line.empty()) {
      continue;
    }
    std::istringstream row(line);
    std::string index;
    std::string gene;
    if (!std::getline(row, index, '\t') || !std::getline(row, gene, '\t')) {
      fail("malformed target-row line: " + line);
    }
    targets.push_back({static_cast<std::uint32_t>(std::stoul(index)), gene});
  }
  if (targets.empty()) {
    fail("target-row file contains no targets");
  }
  return targets;
}

struct ColumnMap {
  std::vector<std::int32_t> group_by_column;
  std::vector<std::uint32_t> cells_by_group;
};

ColumnMap read_column_map(const std::string& path) {
  std::ifstream input(path);
  if (!input) {
    fail("cannot open column-group file: " + path);
  }
  std::string line;
  std::getline(input, line);
  std::vector<std::pair<std::uint32_t, std::uint32_t>> entries;
  std::uint32_t max_column = 0;
  std::uint32_t max_group = 0;
  while (std::getline(input, line)) {
    if (line.empty()) {
      continue;
    }
    std::istringstream row(line);
    std::string column;
    std::string group;
    if (!std::getline(row, column, '\t') || !std::getline(row, group, '\t')) {
      fail("malformed column-group line: " + line);
    }
    const auto column_id = static_cast<std::uint32_t>(std::stoul(column));
    const auto group_id = static_cast<std::uint32_t>(std::stoul(group));
    entries.emplace_back(column_id, group_id);
    max_column = std::max(max_column, column_id);
    max_group = std::max(max_group, group_id);
  }
  if (entries.empty()) {
    fail("column-group file contains no eligible cells");
  }
  ColumnMap result;
  result.group_by_column.assign(static_cast<std::size_t>(max_column) + 1U, -1);
  result.cells_by_group.assign(static_cast<std::size_t>(max_group) + 1U, 0);
  for (const auto& entry : entries) {
    if (result.group_by_column[entry.first] != -1) {
      fail("duplicate eligible matrix column: " + std::to_string(entry.first));
    }
    result.group_by_column[entry.first] = static_cast<std::int32_t>(entry.second);
    result.cells_by_group[entry.second] += 1U;
  }
  return result;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 4) {
    std::cerr << "Usage: " << argv[0]
              << " COLUMN_GROUPS.tsv TARGET_ROWS.tsv OUTPUT.tsv < matrix.mtx\n";
    return 2;
  }

  const auto columns = read_column_map(argv[1]);
  const auto targets = read_targets(argv[2]);
  std::unordered_map<std::uint32_t, std::size_t> target_lookup;
  for (std::size_t index = 0; index < targets.size(); ++index) {
    if (!target_lookup.emplace(targets[index].row, index).second) {
      fail("duplicate target row: " + std::to_string(targets[index].row));
    }
  }

  char header[4096];
  if (std::fgets(header, sizeof(header), stdin) == nullptr ||
      std::string(header).rfind("%%MatrixMarket matrix coordinate integer", 0) != 0) {
    fail("stdin is not an integer coordinate Matrix Market file");
  }
  do {
    if (std::fgets(header, sizeof(header), stdin) == nullptr) {
      fail("missing Matrix Market dimensions");
    }
  } while (header[0] == '%');

  std::uint64_t n_rows = 0;
  std::uint64_t n_columns = 0;
  std::uint64_t expected_nonzero = 0;
  {
    std::istringstream dimensions(header);
    dimensions >> n_rows >> n_columns >> expected_nonzero;
    if (!dimensions || n_rows == 0 || n_columns == 0) {
      fail("invalid Matrix Market dimensions");
    }
  }
  if (columns.group_by_column.size() > n_columns + 1U) {
    fail("column-group map exceeds matrix column count");
  }
  for (const auto& target : targets) {
    if (target.row > n_rows) {
      fail("target row exceeds matrix row count: " + target.gene);
    }
  }

  const std::size_t n_groups = columns.cells_by_group.size();
  const std::size_t n_targets = targets.size();
  std::vector<std::uint64_t> library_totals(n_groups, 0);
  std::vector<std::uint64_t> target_counts(n_groups * n_targets, 0);
  std::vector<std::uint32_t> detected_cells(n_groups * n_targets, 0);

  FastUnsignedReader reader;
  std::uint32_t matrix_row = 0;
  std::uint32_t matrix_column = 0;
  std::uint32_t value = 0;
  std::uint64_t seen_nonzero = 0;
  while (reader.next(matrix_row)) {
    if (!reader.next(matrix_column) || !reader.next(value)) {
      fail("truncated Matrix Market coordinate triple");
    }
    ++seen_nonzero;
    if (matrix_column >= columns.group_by_column.size()) {
      continue;
    }
    const auto group = columns.group_by_column[matrix_column];
    if (group < 0) {
      continue;
    }
    library_totals[static_cast<std::size_t>(group)] += value;
    const auto target = target_lookup.find(matrix_row);
    if (target == target_lookup.end()) {
      continue;
    }
    const auto offset = static_cast<std::size_t>(group) * n_targets + target->second;
    target_counts[offset] += value;
    detected_cells[offset] += 1U;
  }
  if (seen_nonzero != expected_nonzero) {
    fail("nonzero count mismatch: expected " + std::to_string(expected_nonzero) +
         ", parsed " + std::to_string(seen_nonzero));
  }

  std::ofstream output(argv[3]);
  if (!output) {
    fail("cannot open output: " + std::string(argv[3]));
  }
  output << "group_idx\tgene\traw_count\tlibrary_total\tn_cells\tdetected_cells\n";
  for (std::size_t group = 0; group < n_groups; ++group) {
    for (std::size_t target = 0; target < n_targets; ++target) {
      const auto offset = group * n_targets + target;
      output << group << '\t' << targets[target].gene << '\t'
             << target_counts[offset] << '\t' << library_totals[group] << '\t'
             << columns.cells_by_group[group] << '\t' << detected_cells[offset]
             << '\n';
    }
  }

  std::cerr << "parsed_nonzero=" << seen_nonzero << " groups=" << n_groups
            << " targets=" << n_targets << '\n';
  return 0;
}
