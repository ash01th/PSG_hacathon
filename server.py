from flask import Flask, request, jsonify
from llm_completion import get_response_from_llama
import os

#creating document store to store files from users
DOC_STORE = os.path.join(os.getcwd(), 'doc_store')
os.makedirs(DOC_STORE, exist_ok=True)


#api_server defenition and paths
app = Flask(__name__)


#root path - has no use
@app.route('/')
def home():
    return "Hello, Flask!"

#user query is sent here
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    result = get_response_from_llama(data)
    return jsonify(result)  

#user files are sent here 
@app.route('/upload', methods=['POST'])
def upload_file():
    #raise error if no file 
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    #store file in doc_store folder
    file_path = os.path.join(DOC_STORE,"rec"+file.filename)
    file.save(file_path)
    
    return jsonify({"message": "File successfully uploaded"})



if __name__ == '__main__':
    app.run(debug=True)