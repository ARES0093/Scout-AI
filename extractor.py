import os
import docx
from PyPDF2 import PdfReader

def extract_text_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    # --- 1. Handle PDFs ---
    if file_extension == ".pdf":
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None

    # --- 2. Handle Word Documents ---
    elif file_extension == ".docx":
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error reading Word Doc: {e}")
            return None

    # --- 3. Handle Text Files ---
    elif file_extension == ".txt":
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading Text file: {e}")
            return None

    # --- 4. Catch Unsupported Files ---
    else:
        print(f"Skipping {file_path}: Unsupported file type.")
        return None