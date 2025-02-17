import tkinter as tk

from client import send_login_data,send_messages


def login(username,password):
    send_login_data(username,password)
def send_message_to_server(message):
    send_messages(message)
def runLogin():
    global loginWindow
    loginWindow = tk.Tk()

    loginWindow.title("Communication APP - Login")

    screen_width = loginWindow.winfo_screenwidth()
    screen_height = loginWindow.winfo_screenheight()
    loginWindow.resizable(False, False)


    window_width = 300
    window_height = 200

    # Obliczenie pozycji do wyśrodkowania okna
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    loginWindow.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")


    username_label = tk.Label(loginWindow, text="Username:")
    username_label.pack(pady=5)

    username_entry = tk.Entry(loginWindow, font=("Arial", 12))
    username_entry.pack(pady=5)


    password_label = tk.Label(loginWindow, text="Password:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(loginWindow, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)


    login_button = tk.Button(loginWindow, text="Login", command=lambda: login(username_entry.get(),password_entry.get()) )
    login_button.pack(pady=10)
    loginWindow.mainloop()

def destroy_login_window():
    if loginWindow:
        loginWindow.destroy()
def destroy_main_window():
    if root:
        root.destroy()
def runMainWindow():
    global root
    root = tk.Tk()
    root.title("CommunicationApp")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.resizable(False, False)

    # Rozmiar okna
    window_width = 900
    window_height = 500

    # Obliczenie pozycji do wyśrodkowania okna
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    # Ustawienie wielkości i pozycji okna
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")


    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)


    global user_list
    user_list = tk.Listbox(root, width=20, bg="lightgrey", font=("Arial", 10,"bold"),foreground="red",justify="center")
    user_list.grid(row=0, column=2, rowspan=1, sticky="ns", padx= 10, pady=10)



    global chat_window
    chat_window = tk.Text(root, wrap=tk.WORD, font=("Arial", 10))
    chat_window.grid(row=0, column=1, sticky="nsew", padx=10,pady=10)
    chat_window.config(state=tk.DISABLED)


    chat_window.tag_configure("time", foreground='green')
    chat_window.tag_configure("nickname", foreground='red')
    chat_window.tag_configure("msg", foreground='black')
    chat_window.tag_configure("private", foreground='#FF6EC7')


    input_field = tk.Text(root, font=("Arial", 12), bg="lightgray" ,height=2)
    input_field.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    input_field.config(font=("Segoe UI Emoji", 12))

    send_button = tk.Button(root, text="Send", command=lambda: send_message_to_server(input_field.get(1.0,"end").strip()), bg="lightblue", font=("Arial", 10))
    send_button.grid(row=1, column=2, sticky="nsew", padx=10, pady= 10)

    root.mainloop();

def add_message_to_chat(message):
    chat_window.config(state=tk.NORMAL)
    parts = message.split("-")

    if len(parts) == 3:
        time = "- " + parts[0] + "\n"
        nickname = parts[1] + " "
        msg = " " +parts[2] + "\n"

        chat_window.insert(tk.END, nickname, "nickname")
        chat_window.insert(tk.END, time, "time")
        chat_window.insert(tk.END, msg, "msg")
    elif message.startswith("PRIV"):
        chat_window.insert(tk.END, message+"\n", "private")


    else:
        chat_window.insert(tk.END, message + "\n", "message")
    chat_window.see(tk.END)
    chat_window.config(state=tk.DISABLED)

def active_users_list(users):
    user_list.delete(0, tk.END)
    user_list.insert(tk.END, "ACTIVE")
    for user in users:
        user_list.insert(tk.END, "•"+user)

