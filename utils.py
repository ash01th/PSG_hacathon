import PyPDF2
import docx
import os
import json
import nltk
from nltk.tokenize import word_tokenize
from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.Client()
collection = client.create_collection("embeddings3333")
# Download files required for tokenization
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

#setting a threshold of 6000 tokens and checking if embedding is needed
def optional_embedding(text):
    if count_tokens(text)<6000:
        return {"text":"Text is within the token limit"}
    else:
        return {"embeddings":"N/A"}

#creating chunks of approximately 5000 characters long , with 1000 character overlap
def split_text_into_chunks(text, file_name, chunk_size=5000, chunk_overlap=1000, separator=" "):
    splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator=separator
    )
    chunks = splitter.split_text(text)
    
    # Ensure the directory exists
    os.makedirs('chunk_store', exist_ok=True)
    
    # Store each chunk as a JSON object in the specified folder
    for i, chunk in enumerate(chunks):
        chunk_data = {f"{file_name}_chunk_{i + 1}": chunk}
        with open(f'chunk_store/{file_name}_chunk_{i + 1}.json', 'w') as f:
            json.dump(chunk_data, f)
    
    return chunks

def create_embeddings(text,type):
    query_prompt_name = "s2p_query"
    model = SentenceTransformer("dunzhang/stella_en_400M_v5", trust_remote_code=True,device="cpu",config_kwargs={"use_memory_efficient_attention": False, "unpad_inputs": False})
    if type=="query":
        return(model.encode(text, prompt_name=query_prompt_name))
    else:
        return(model.encode(text))

def store_embeddings_in_chromadb(text,embeddings,file_name):
    collection = client.get_collection("embeddings3333")
#    embedding = create_embeddings(text,
    collection.add(
        documents=text,    # List of documents (texts)
        embeddings=embeddings,  # Corresponding embeddings
        ids=file_name  # Unique IDs for each document
    )

def get_relevant_data(user_query):
    embedding=create_embeddings(user_query,type="query")
    collection = client.get_collection("embeddings3333")
    results = collection.query(
    query_embeddings=[embedding],  # Query embeddings
    n_results=1  # Number of results to return
    )
    return results

