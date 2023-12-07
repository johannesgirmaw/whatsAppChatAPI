import requests
import json

def create_chatroom():
    url = "http://localhost:8000/text_chat/"

    # Data for creating a chatroom
    data = {
        "name": "Sample Chatroom",
        "max_members": 10
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Sending the HTTP POST request
        response = requests.post(url, data=json.dumps(data), headers=headers)

        # Check (status code 2xx)
        if response.status_code // 100 == 2:
            print("Chatroom created successfully.")
            print("Response:", response.json())
        else:
            print("Error:", response.text)

    except Exception as e:
        print("An error occurred:", str(e))

# Call the function to create a chatroom
create_chatroom()


