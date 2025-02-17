import socket
import threading
import time
import sqlite3
import traceback

clients = []
connected_users = {}

def save_logs(username, message):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO logs (date_time, username, message) VALUES (?, ?, ?)",
                       (time.strftime("%d-%m-%Y %H:%M:%S"), username, message))
        conn.commit()
    finally:
        conn.close()

def save_logs_priv(sender, destination, message):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO logs_private (date_time, sender, destination, message) VALUES (?, ?, ?, ?)",
                       (time.strftime("%d-%m-%Y %H:%M:%S"), sender, destination, message))
        conn.commit()
    finally:
        conn.close()

def load_history(client_socket):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    query = """
        SELECT date_time, username AS user, message, 'public' AS message_type
        FROM logs
        WHERE username NOT LIKE 'System'
        UNION ALL
        SELECT date_time, destination AS user, message, 'private' AS message_type
        FROM logs_private
        WHERE sender = ? OR destination = ?
        ORDER BY date_time;
        """
    cursor.execute(query, (connected_users.get(client_socket), connected_users.get(client_socket)))
    results = cursor.fetchall()
    conn.close()

    if results:
        for rows in results:
            if rows[3] == 'public':
                time_str = rows[0].split(" ")[1]
                message = time_str + "-" + rows[1] + "-" + rows[2]
            elif rows[3] == 'private':
                if rows[1] == connected_users.get(client_socket):
                    message = "PRIV FROM " + rows[1] + ": " + rows[2]
                else:
                    message = "PRIV TO " + rows[1] + ": " + rows[2]
            client_socket.send((message + "\n").encode('utf-8'))

def recive_login_data(client_socket):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        login_data = client_socket.recv(1024).decode("utf-8").strip().split(":")
        print(login_data)
        username = login_data[0]
        password = login_data[1]

        cursor.execute("SELECT username, password FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()

        if result is None:
            client_socket.send("False".encode('utf-8'))
            return None
        elif username not in connected_users.values():
            client_socket.send("True".encode('utf-8'))
            connected_users[client_socket] = username
            return username
    except Exception as e:
        print(f"Error receiving login data: {e}")
        return None
    finally:
        conn.close()

def broadcast(message, sender_socket=None, destination_socket=None):
    try:
        if sender_socket is None and destination_socket is None:
            for client in clients:
                try:
                    client.sendall((message + "\n").encode('utf-8'))
                except Exception as e:
                    print(f"Error sending message to {client}: {e}")
                    clients.remove(client)
        else:
            for client in clients:
                if client == sender_socket:
                    message_sender = f"PRIV TO {connected_users.get(destination_socket)}: " + message + "\n"
                    client.sendall(message_sender.encode('utf-8'))
                elif client == destination_socket:
                    message_dest = f"PRIV FROM {connected_users.get(sender_socket)}: " + message + "\n"
                    client.sendall(message_dest.encode('utf-8'))
    except Exception as e:
        print(e)

def active_users_info():
    try:
        active_users_send = "active: ," + ",".join(connected_users.values())
        broadcast(active_users_send)
    except Exception as e:
        print(f"Error sending active user list: {e}")

def get_key_by_value(value):
    for key, val in connected_users.items():
        if val == value:
            return key
    return None

def handle_client(client_socket, client_address):
    username = recive_login_data(client_socket)
    if username is None:
        client_socket.close()
        return

    time.sleep(1)
    load_history(client_socket)
    welcome_message = f"User {username} dołączył do czatu."
    save_logs("System", welcome_message)
    broadcast(welcome_message)
    active_users_info()

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8').strip()
            if message.startswith("/"):
                if message.startswith("/priv"):
                    parts = message.split(" ")
                    destination = parts[1]
                    message_to_send = " ".join(parts[2:])
                    if destination == connected_users.get(client_socket):
                        client_socket.sendall("PRIV TO: You cannot send a private message to yourself\n".encode('utf-8'))
                    elif destination in connected_users.values():
                        save_logs_priv(username, destination, message_to_send)
                        broadcast(message_to_send, client_socket, get_key_by_value(destination))
                    else:
                        client_socket.sendall(f"{destination}: User is not online\n".encode('utf-8'))
                elif message == "/exit":
                    break
                else:
                    client_socket.sendall("Unknown command\n".encode('utf-8'))
            else:
                formatted_message = f"{time.strftime('%H:%M:%S')}-{username}-{message}"
                save_logs(username, message)
                broadcast(formatted_message)
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Error handling user: {e}")
            traceback.print_exc()
            break

    leave_message = f"User {username} left the chat."
    save_logs("System", leave_message)
    broadcast(leave_message)
    active_users_info()
    client_socket.close()
    connected_users.pop(client_socket, None)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 2137))
server_socket.listen(10)
print("Server is listening...")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
finally:
    server_socket.close()
