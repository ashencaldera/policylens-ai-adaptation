import re
from PyPDF2 import PdfReader

def extract_and_clean_pdf(pdf_file):
    """
    Extracts text from PDF and applies NLP preprocessing.
    """
    reader = PdfReader(pdf_file)
    raw_text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            raw_text += content
            
    # Preprocessing: Remove excessive whitespace and repetitive artifacts
    cleaned_text = re.sub(r'\s+', ' ', raw_text)  # Normalize spaces
    cleaned_text = re.sub(r'Page \d+ of \d+', '', cleaned_text) # Remove page footers
    
    return cleaned_text.strip()

# text stats
def get_text_stats(text):
    """
    Provides basic NLP stats to demonstrate text analysis for the Viva.
    """
    if text is None:
        return 0, 0
    words = text.split()
    return len(words), len(text)