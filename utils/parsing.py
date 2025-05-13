import os
import pdfplumber
import docx2txt

def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from a file based on its extension.
    Supports PDF, DOCX, and TXT files.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Extracted text as a string, or empty string if extraction fails
    """
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        # Extract text from PDF
        if file_ext == '.pdf':
            text = extract_from_pdf(file_path)
        
        # Extract text from DOCX
        elif file_ext == '.docx':
            text = extract_from_docx(file_path)
        
        # Read text file directly
        elif file_ext == '.txt':
            text = extract_from_txt(file_path)
        
        # Unsupported file type
        else:
            print(f"Unsupported file type: {file_ext}")
            return ""
        
        # Clean up text
        text = clean_text(text)
        return text
    
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""

def extract_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file"""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file"""
    return docx2txt.process(file_path)

def extract_from_txt(file_path: str) -> str:
    """Read text from a TXT file"""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

def clean_text(text: str) -> str:
    """Clean extracted text by removing extra whitespace"""
    if not text:
        return ""
    
    # Replace multiple newlines with a single one
    import re
    text = re.sub(r'\n+', '\n', text)
    
    # Replace multiple spaces with a single one
    text = re.sub(r' +', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text
