# Communication App 🚀

A simple real-time messaging app built with Python! With this app, you can send public and private messages, and the entire thing runs on a cool GUI made with `tkinter` and uses `SQLite` for the database!

## What can the app do? 🔥

- **Login**: Users log in with a username and password.
- **Public chat**: Send messages visible to everyone.
- **Private messages**: Send private messages to specific users.
- **Active user list**: See who's online.
- **Chat history**: All messages (public and private) are saved in the database.

## Requirements 💻

- Python 3.x
- Tkinter (for GUI)
- SQLite (for the database)

## How to use it? 💬

### Server
The server runs on port `2137` and handles incoming client connections. It manages login, message sending, and logs everything in the database (`users.db`). It can handle multiple users at once.

### Client
- **Login**: Enter your username and password. If they are correct, you’ll proceed to the chat app!
- **Public chat**: Type your message in the chat window and click **Send** to broadcast it to everyone online.
- **Private messages**: Type `/priv <username> <message>` to send a private message to a specific user.
- **Exit**: To leave the chat, type `/exit` – your connection will be closed.

### Message history
The server stores all messages in the database, so you can view the entire chat history, including both public and private messages.

## Inside the Code 📂

### `server.py`
The server script is responsible for:
- Handling client connections on port `2137`.
- Managing user login and authentication.
- Storing chat history (public and private messages) in the `users.db` SQLite database.
- Broadcasting messages to all connected clients or sending private messages to specific users.

### `client.py`
This file handles the client-side logic:
- Establishing a connection with the server.
- Sending login credentials to the server.
- Receiving messages from the server and displaying them.
- Allowing users to send messages (both public and private) to the server.

### `gui.py`
Contains the graphical user interface (GUI) built using `tkinter`. It provides:
- A login window where users can input their username and password.
- The main chat window where messages are displayed.
- An input area to send messages and interact with the chat.
- A sidebar showing the list of active users.

### `users.db`
This SQLite database stores all the necessary information:
- User credentials (username and password).
- All messages (public and private) sent by users, along with timestamps.

## 🎩 Author
Daiwd Zwolak