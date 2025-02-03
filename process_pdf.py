# process_pdf.py
import os
import asyncio
from dotenv import load_dotenv
from pyzerox import zerox

# Load environment variables from .env file
load_dotenv()

# Retrieve model and API key from the environment
MODEL = os.getenv("MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY must be set in the .env file")

# Ensure the key is in os.environ for pyzerox to pick it up
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

async def process_pdf(pdf_path: str, output_dir: str = None) -> str:
    """
    Processes a single PDF file using py-zerox and returns the concatenated Markdown content.
    """
    result = await zerox(
        file_path=pdf_path,
        model=MODEL,
        output_dir=output_dir,
        maintain_format=False  # Set True if cross-page formatting context is needed.
    )
    # Use attribute access on each Page object
    markdown_content = "\n".join(page.content for page in result.pages if page.content)
    return markdown_content

# For testing:
if __name__ == "__main__":
    import sys
    pdf_file = sys.argv[1] if len(sys.argv) > 1 else "sample.pdf"
    markdown = asyncio.run(process_pdf(pdf_file))
    print(markdown)
