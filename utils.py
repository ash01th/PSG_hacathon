import PyPDF2
import docx
import os
import nltk
from nltk.tokenize import word_tokenize

#download files required for tokenization
nltk.download('punkt')
nltk.download('punkt_tab')

# Create a folder called chunks_store if it does not already exist
CHUNKS_FOLDER = os.path.join(os.getcwd(), 'chunks_store')
os.makedirs(CHUNKS_FOLDER, exist_ok=True)

def extract_text(file_path):
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension.lower() == '.docx':
        return extract_text_from_word(file_path)
    elif file_extension.lower() == '.txt':
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_text_from_word(docx_path):
    doc = docx.Document(docx_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r') as file:
        text = file.read()
    return text  

#count tokens to make sure it does not exceed context window
def count_tokens(text):
    tokens = word_tokenize(text)
    return len(tokens)

#setting a threshold of 6000 tokens
def optional_embedding(text):
    if count_tokens(text)<6000:
        return {"text":text}
    else:
        return {"embeddings":"N/A"}


    



