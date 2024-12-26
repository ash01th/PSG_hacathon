from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq
from dotenv import load_dotenv
import sys

from inference import answer_followup
from inference import get_inference
from llm_completion import get_response_from_llama
print(os.getcwd())
# Create a document store to store files from users
DOC_STORE = os.path.join(os.getcwd(), 'doc_store')
os.makedirs(DOC_STORE, exist_ok=True)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# API server definition and paths
app = Flask(__name__)
CORS(app)  # Allow all cross-origin requests by default

# Load environment variables
load_dotenv(dotenv_path='api_key.env')
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Messages sent to LLM (sample input)
msg1 = [
    {
        "role": "system",
        "content": "you are a helpful assistant."
    },
    {
        "role": "user",
        "content": "Explain the importance of fast language models",
    }
]


# Root path - has no use
@app.route('/')
def home():
    return "Hello, Flask!"

# User query is sent here
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    try:
        print("called")
        query=data["userInput"]
        print(query)
        history = data["chatHistory"]
        print(history)
        file_names = [f for f in os.listdir('uploads') if os.path.isfile(os.path.join('uploads', f))]
        filename='uploads/'+file_names[0]
        if len(history) == 0:
            print("2")
            result= get_inference(query,filename)
            print(result)
            return jsonify({"response": result}), 200
        else:
            print("3")
            result=answer_followup(query,filename,history)
            print(result)
            return jsonify({"response": result}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# User files are sent here
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # Define allowed file extensions
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed: {file.filename}'}), 400

    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # Save the file safely
        file.save(file_path)
    except Exception as e:
        return jsonify({'error': f'Failed to upload {file.filename}: {str(e)}'}), 500

    # Create a sample newConversation data structure
    new_conversation = {
        "message": "File uploaded successfully",
        "uploaded_file": file.filename
    }

    return jsonify({'newConversation': new_conversation}), 200

# Delete all files
@app.route('/delete', methods=['POST'])
def delete_files():
    print("hi")  # This should print to the console when the route is hit
    try:
        # Specify the folder where files are stored
        upload_folder = os.path.join(os.getcwd(), 'uploads')
        print(f"Files will be deleted from: {upload_folder}")  # Log the path

        # Delete all files in the folder
        files_deleted = []
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                files_deleted.append(filename)
        
        # Return a list of deleted files
        return jsonify({"message": "File deleted successfully", "deleted_files": files_deleted}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log any errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
