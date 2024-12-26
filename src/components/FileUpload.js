import React, { useState, useEffect } from "react";
import Dropzone from "react-dropzone";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  useEffect(() => {
    const savedFile = JSON.parse(localStorage.getItem("selectedFile"));
    if (savedFile) {
      setFile(savedFile);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("selectedFile", JSON.stringify(file));
  }, [file]);

  const handleDrop = (acceptedFiles) => {
    const selectedFile = acceptedFiles[0]; // Restrict to one file
    setFile(selectedFile); 
    localStorage.setItem("selectedFile", JSON.stringify(selectedFile)); // Save to localStorage
  };
  

  const handleUpload = async () => {
    const formData = new FormData();
    if (file) {
      formData.append("file", file); // Attach the single file object

      try {
        setUploadStatus("Uploading...");
        const response = await axios.post("http://192.168.241.174:5000/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        if (response.data?.newConversation) {
          setUploadStatus("Upload successful!");
        } else {
          setUploadStatus("Upload failed.");
        }
      } catch (error) {
        console.error(error);
        setUploadStatus("Upload failed.");
      }
    } else {
      setUploadStatus("No file selected.");
    }
  };

  const handleDelete = async () => {
    try {
      const response = await axios.post("http://192.168.241.174:5000/delete");
      console.log(response.data); // Log the server response to debug
  
      if (response.data?.message === "File deleted successfully") {
        setFile(null); // Clear the file in the component's state
        localStorage.removeItem("selectedFile"); // Remove the file from localStorage
        setUploadStatus("File deleted.");
      } else {
        setUploadStatus("Failed to delete file.");
      }
    } catch (error) {
      console.error(error);
      setUploadStatus("Failed to delete file on the server.");
    }
  };  
  

  return (
    <div style={{ padding: "20px", borderRadius: "8px", boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)" }}>
      <Dropzone onDrop={handleDrop}>
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
            }}
          >
            <input {...getInputProps()} />
            <p>Drag and drop a file here, or click to select a file</p>
          </div>
        )}
      </Dropzone>

      {file && (
        <div style={{ marginTop: "20px" }}>
          <h4>Selected File:</h4>
          <p>
            {file.name} - {(file.size / 1024).toFixed(2)} KB
          </p>
        </div>
      )}

      <button
        onClick={handleUpload}
        style={{
          marginTop: "15px",
          backgroundColor: "#8CE069",
          padding: "10px",
          borderRadius: "5px",
          color: "white",
          border: "none", // Remove the default border
          outline: "none", // Remove the focus outline
          cursor: "pointer", // Add a pointer cursor for better UX
        }}
      >
        Upload
      </button>

      {file && (
        <button
          onClick={handleDelete}
          style={{
            marginTop: "15px",
            backgroundColor: "#f44336",
            padding: "10px",
            borderRadius: "5px",
            color: "white",
            marginLeft: "10px",
            border: "none", // Remove the default border
            outline: "none", // Remove the focus outline
            cursor: "pointer", // Add a pointer cursor for better UX
          }}
        >
          Delete File
        </button>
      )}
      {uploadStatus && <p style={{ marginTop: "10px" }}>{uploadStatus}</p>}
    </div>
  );
};

export default FileUpload;
