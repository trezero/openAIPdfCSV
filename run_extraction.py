# run_extraction.py
import os
import asyncio
from process_pdf import process_pdf
from markdown_to_csv import extract_markdown_tables, write_tables_to_csv

PDF_DIRECTORY = "./invSmall"  # folder where your PDF files reside
CSV_OUTPUT = "combined_output.csv"

async def process_all_pdfs(pdf_dir: str) -> list:
    """
    Processes all PDFs in the specified directory.
    Returns a list of all tables (each table is a list of rows).
    """
    all_tables = []
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            print(f"Processing {pdf_path}...")
            try:
                markdown = await process_pdf(pdf_path)
                tables = extract_markdown_tables(markdown)
                if tables:
                    print(f"Found {len(tables)} table(s) in {filename}.")
                    all_tables.extend(tables)
                else:
                    print(f"No tables found in {filename}.")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return all_tables

def main():
    all_tables = asyncio.run(process_all_pdfs(PDF_DIRECTORY))
    if all_tables:
        write_tables_to_csv(all_tables, CSV_OUTPUT)
        print(f"CSV file written to {CSV_OUTPUT}")
    else:
        print("No tables extracted.")

if __name__ == "__main__":
    main()
