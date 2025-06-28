# Main entry point for the AI-powered Question Paper Generator & Exam Pattern Analyzer

from src.ingest import DocumentIngestor

def main():
    print("Welcome to the AI-powered Question Paper Generator & Exam Pattern Analyzer!")
    print("This is a placeholder for the CLI or web interface.")
    # TODO: Add CLI or web interface logic here

    pdf_path = "path/to/your/file.pdf"
    ingestor = DocumentIngestor(pdf_path)
    text_list = ingestor.parse_pdf()

    for page_text in text_list:
        print(page_text)

if __name__ == "__main__":
    main() 