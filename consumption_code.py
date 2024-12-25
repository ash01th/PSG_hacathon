import requests

# List of dictionaries to be sent
msg1=[
    {
        "role": "system",
        "content": "you are a helpful assistant."
    },
    {
        "role": "user",
        "content": "Explain the importance of fast language models",
    }
]


# URL of the /process API endpoint
"""url = "http://localhost:5000/process"

# Sending the POST request
response = requests.post(url, json=msg1)

# Checking the response
if response.status_code == 200:
    print("Data sent successfully!")
    print("Response:", response.json())
else:
    print("Failed to send data. Status code:", response.status_code)
    print("Response:", response.text)


"""
# Path to the file to be sent
file_path = 'file.txt'

# URL of the /file_upload API endpoint
url = "http://localhost:5000/upload"

# Opening the file in binary mode
with open(file_path, 'rb') as file:
    # Sending the POST request with the file
    response = requests.post(url, files={'file': file})

# Checking the response
if response.status_code == 200:
    print("File sent successfully!")
    print("Response:", response.json())
else:
    print("Failed to send file. Status code:", response.status_code)
    print("Response:", response.text)