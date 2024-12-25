import React, { useState } from "react";
import Dropzone from "react-dropzone";
import axios from "axios";

const FileUpload = ({ onFileUpload }) => {
  const [files, setFiles] = useState([]);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleDrop = (acceptedFiles) => {
    setFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);  // Add new files to the existing files state
  };

  const handleUpload = async () => {
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      setUploadStatus("Uploading...");
      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // Response contains the new conversation data
      onFileUpload(response.data.newConversation);
      setUploadStatus("Upload successful!");
    } catch (error) {
      console.error(error);
      setUploadStatus("Upload failed.");
    }
  };

  return (
    <div style={{ padding: "20px", borderRadius: "8px", boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)" }}>
      <Dropzone onDrop={handleDrop} multiple={true}>
        {({ getRootProps, getInputProps }) => (
            <div
            {...getRootProps()}
            style={{
                border: "2px dashed #ccc",
                padding: "30px",
                textAlign: "center",
                cursor: "pointer",
                borderRadius: "8px",
                backgroundColor: "#f9f9f9",
                transition: "background-color 0.3s ease",
            }}
            onDragEnter={(e) => e.target.style.backgroundColor = "#f1f1f1"}
            onDragLeave={(e) => e.target.style.backgroundColor = "#f9f9f9"}
            >
            <input {...getInputProps()} />
            <p>Drag and drop files here, or click to select files</p>
            </div>
        )}
        </Dropzone>

      {/* Display selected files */}
      {files.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h4>Selected Files:</h4>
          <ul>
            {files.map((file, index) => (
              <li key={index} style={{ color: "#555" }}>
                {file.name} - {Math.round(file.size / 1024)} KB {/* Display file size in KB */}
              </li>
            ))}
          </ul>
        </div>
      )}

      <button
        onClick={handleUpload}
        style={{
          padding: "12px",
          marginTop: "15px",
          backgroundColor: "#8CE069",
          color: "white",
          border: "none",
          cursor: "pointer",
          borderRadius: "5px",
          fontSize: "1em",
        }}
      >
        Upload
      </button>
      {uploadStatus && <p style={{ marginTop: "10px", color: "#555" }}>{uploadStatus}</p>}
    </div>
  );
};

export default FileUpload;
