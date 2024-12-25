import React, { useState, useEffect } from "react";
import Dropzone from "react-dropzone";
import axios from "axios";

const FileUpload = () => {
  const [files, setFiles] = useState([]);
  const [uploadStatus, setUploadStatus] = useState("");

  // Load files from localStorage when the component mounts
  useEffect(() => {
    const savedFiles = JSON.parse(localStorage.getItem("selectedFiles"));
    if (savedFiles) {
      setFiles(savedFiles); // Directly set metadata from localStorage
    }
  }, []);

  // Save files to localStorage whenever the files state changes
  useEffect(() => {
    if (files.length > 0) {
      const filesData = files.map((file) => ({
        name: file.name,
        size: file.size,
        type: file.type,
      }));
      localStorage.setItem("selectedFiles", JSON.stringify(filesData));
    } else {
      localStorage.removeItem("selectedFiles"); // Clear storage if no files
    }
  }, [files]);

  const handleDrop = (acceptedFiles) => {
    const newFiles = acceptedFiles.map((file) => ({
      name: file.name,
      size: file.size,
      type: file.type,
    }));
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    files.forEach((file) => formData.append("files", new Blob([], { type: file.type }), file.name));

    try {
      setUploadStatus("Uploading...");
      await axios.post("http://localhost:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setUploadStatus("Upload successful!");
    } catch (error) {
      console.error(error);
      setUploadStatus("Upload failed.");
    }
  };

  const handleDelete = async () => {
    try {
      await axios.post("http://localhost:5000/delete");

      // After deletion, clear files from the state and localStorage
      setFiles([]);
      setUploadStatus("Files deleted.");
    } catch (error) {
      console.error(error);
      setUploadStatus("Failed to delete files on the server.");
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
            onDragEnter={(e) => (e.target.style.backgroundColor = "#f1f1f1")}
            onDragLeave={(e) => (e.target.style.backgroundColor = "#f9f9f9")}
          >
            <input {...getInputProps()} />
            <p>Drag and drop files here, or click to select files</p>
          </div>
        )}
      </Dropzone>

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

      {files.length > 0 && (
        <button
          onClick={handleDelete}
          style={{
            padding: "12px",
            marginTop: "15px",
            backgroundColor: "#f44336",
            color: "white",
            border: "none",
            cursor: "pointer",
            borderRadius: "5px",
            fontSize: "1em",
            marginLeft: "10px",
          }}
        >
          Delete Files
        </button>
      )}

      {uploadStatus && <p style={{ marginTop: "10px", color: "#555" }}>{uploadStatus}</p>}
    </div>
  );
};

export default FileUpload;
