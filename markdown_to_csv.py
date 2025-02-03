# markdown_to_csv.py
import re
import csv

def extract_markdown_tables(markdown: str) -> list:
    """
    Finds markdown table blocks in the text.
    Returns a list of tables, each table is a list of rows (each row is a list of cell strings).
    """
    tables = []
    # Regex to identify table blocks:
    # Look for at least three lines: header, divider, and one data row.
    table_pattern = re.compile(
        r"((?:^\|.*\n)+)",  # one or more lines starting with | at the beginning of line
        re.MULTILINE
    )
    
    for match in table_pattern.finditer(markdown):
        block = match.group(1)
        lines = block.strip().splitlines()
        # A valid table should have at least a header and divider row.
        if len(lines) < 2:
            continue
        # Check that the second line is a divider (contains ---)
        if not re.search(r":?-{3,}:?", lines[1]):
            continue
        # Process each line: split on pipe and strip whitespace; remove empty entries due to leading/trailing pipes.
        table = []
        for line in lines:
            # Remove leading and trailing pipes, then split
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            table.append(cells)
        tables.append(table)
    return tables

def write_tables_to_csv(tables: list, csv_filepath: str):
    """
    Writes a list of tables into a single CSV file using unified headers.
    """
    header_set = set()
    all_rows = []
    
    # Phase 1: Collect all headers and data rows
    for table in tables:
        if not table:
            continue
        header = table[0]
        header_set.update(header)
        for row in table[1:]:
            all_rows.append((header, row))
    
    # Create unified headers (sorted for consistency)
    unified_header = sorted(header_set)
    
    # Phase 2: Write all data with unified headers
    with open(csv_filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(unified_header)
        
        for local_header, row in all_rows:
            # Create mapping from local header positions to unified columns
            row_dict = {h: v for h, v in zip(local_header, row)}
            unified_row = [row_dict.get(h, "") for h in unified_header]
            writer.writerow(unified_row)

# Example usage:
if __name__ == "__main__":
    sample_markdown = """
# Invoice 36258
...
| Item                                       | Quantity | Rate   | Amount  |
|--------------------------------------------|----------|--------|---------|
| Global Push Button Manager's Chair, Indigo | 1        | $48.71 | $48.71  |
| Chairs, Furniture, FUR-CH-4421             |          |        |         |
...
    """
    tables = extract_markdown_tables(sample_markdown)
    write_tables_to_csv(tables, "output.csv")
