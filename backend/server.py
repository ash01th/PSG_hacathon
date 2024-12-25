from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow all cross-origin requests by default

# Define the path where files will be uploaded
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/process', methods=['POST'])
def get_bot_response():
    print("Received request:", request.json)
    try:
        data = request.get_json() 
        user_input = data.get('userInput')  
        chat_history = data.get('chatHistory')  
        
        # Dummy response
        bot_response = {"response": "This is a mock response."}

        return jsonify(bot_response) 

    except Exception as e:
        return jsonify({"response": "An error occurred: " + str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('files')
    uploaded_files = []

    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        uploaded_files.append(file.filename)

    # Create a sample newConversation data structure
    new_conversation = {
        "message": "Files uploaded successfully",
        "uploaded_files": uploaded_files
    }

    return jsonify({'newConversation': new_conversation}), 200

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
        return jsonify({"message": "Files deleted successfully", "deleted_files": files_deleted}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log any errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
