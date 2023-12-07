import websocket
import rel
import requests
import json

def login():
    url = "http://localhost:8000/auth/"

    # Data for creating a chatroom
    data = {
        "username": input("Enter Username:"),
        "password": input("Enter password:"),
    }

    try:
        # Sending the HTTP POST request
        response = requests.post(url, data=data)
        print("response:",response, json.loads(response.content.decode('utf-8'))['token'])
        if response:
           return json.loads(response.content.decode('utf-8'))['token']
    except Exception as e:
        print("An error occurred:Incorrect credential username and password, Try again", str(e))


def get_chat_room_list():
    url = "http://localhost:8000/text_chat/"
    try:
        response = requests.get(url)
        if response:
            return json.loads(response.content.decode('utf-8'))
    except Exception as e:
        print("An error occurred:", str(e))



def create_chatroom():
    url = "http://localhost:8000/text_chat/"

    # Data for creating a chatroom
    data = {
        "name": input("Enter the name of the chatroom:"),
        "max_members": input("Enter the maximum number of members:")
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
            return json.loads(response.content.decode('utf-8'))
        else:
            print("Error:", response.text)

    except Exception as e:
        print("An error occurred:", str(e))


def on_message(ws, message):
    print("---------Server----------",message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    # ws.close()
    
def on_open(ws):
    print("Opened connection")
    while True:
        val = input("Please enter your message: ")
        if val == "exit":
            break
        ws.send(f"Client:yes please, '{val}'!")

if __name__ == "__main__":
    websocket.enableTrace(True)
    while True:
        token = login()
        if token:
            break
    
    if token:
        try:
            print("Welcome to your whatsapp")
            
            headers = {
            "Authorization": f"Token {token}"
            }
            room_options = ["1 - Join Chatroom(Select from the list):", "2 - Create Chatroom:"]
            for option in room_options:
                print(option )    
            chose_val = int(input("Please choose:"))
            chat_room_id = 0
            
            if  chose_val == 1:
                for i in get_chat_room_list():
                    print(i['id'],i['name'])
                chat_room_id = input("PLease enter chatroom Id:(1 - )")
                
            elif chose_val == 2:
                chatroom_data = create_chatroom()
                print("chatroom_data:",chatroom_data)
                chat_room_id = chatroom_data['id']
            
            
            ws = websocket.WebSocketApp("ws://localhost:8000/ws/text_chat/" + str(chat_room_id)+"/",
                                        header=headers,
                                        on_open=on_open,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close
                                        )

            ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
            rel.signal(2, rel.abort)  # Keyboard Interrupt
            rel.dispatch()
        except Exception as e:
            print("An error occurred: You should login", str(e))
    