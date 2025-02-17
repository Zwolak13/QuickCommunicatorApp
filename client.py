import socket
import threading
import gui

def send_login_data(username, password):
    global client_sock
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(('localhost', 2137))

        data = f'{username}:{password}'
        client_sock.sendall(data.encode("utf-8"))

        response = client_sock.recv(1024).decode('utf-8')

        if response == "True":
            receive_thread = threading.Thread(target=receive_messages, daemon=True)
            receive_thread.start()
            gui.destroy_login_window()
            gui.runMainWindow()
        else:
            print("Nieprawidłowe dane logowania.")
            client_sock.close()
    except Exception as e:
        print(e)
        if client_sock:
            client_sock.close()

def receive_messages():
    buffer = ""
    while True:
        try:
            data = client_sock.recv(1024).decode("utf-8")
            if not data:
                print("Rozłączono z serwerem.")
                break

            buffer += data
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if message.startswith("active: "):
                    users = message.split(",")[1:]
                    gui.active_users_list(users)
                else:
                    gui.add_message_to_chat(message)
        except Exception as e:
            print(f"Błąd otrzymywania wiadomości: {e}")
            break

def send_messages(message):
    try:
        client_sock.send(message.encode("utf-8"))
        print(f"Wysłano {message} do serwera")

        if message.strip() == "/exit":
            print("Rozłączono z serwerem.")
            gui.destroy_main_window()
            client_sock.close()
    except Exception as e:
        print(f"Błąd wysyłania wiadomości: {e}")

def start_client():
    gui.runLogin()

if __name__ == "__main__":
    start_client()
