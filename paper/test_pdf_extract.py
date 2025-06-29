from src.ingest import DocumentIngestor
import os

PDF_FILE = 'my_question_paper.pdf'  # Change this if your file has a different name

def main():
    print(os.environ['PATH'])
    ingestor = DocumentIngestor(PDF_FILE)
    pages = ingestor.parse_pdf()
    for i, text in enumerate(pages, 1):
        print(f'--- Page {i} ---')
        print(text[:1000])  # Print first 1000 chars for brevity
        print('\n')

if __name__ == '__main__':
    main() 