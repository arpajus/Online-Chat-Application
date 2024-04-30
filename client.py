import threading
from tkinter import *
from tkinter import simpledialog
import grpc
import chat_pb2 as chat
import chat_pb2_grpc as rpc
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class Client:
    def __init__(self, u: str, window, local_ip, local_port):
        self.window = window
        self.username = u
        self.local_ip = local_ip
        self.local_port = local_port
        self.remote_ip = None
        self.remote_port = None
        self._setup_ui()
        self.window.mainloop()

    def connect_to_peer(self):
        if self.remote_ip and self.remote_port:
            address = f'{self.remote_ip}:{self.remote_port}'
            self.channel = grpc.insecure_channel(address)
            self.conn = rpc.ChatServerStub(self.channel)
            threading.Thread(target=self._listen_for_messages, daemon=True).start()

    def _listen_for_messages(self):
        for note in self.conn.ChatStream(chat.Empty()):
            print(f"R[{note.name}] {note.message}")
            self.chat_list.insert(END, f"[{note.name}] {note.message}\n")

    def send_message(self, event):
        message = self.entry_message.get()
        if message != '':
            n = chat.Note()
            n.name = self.username
            n.message = message
            print(f"S[{n.name}] {message}")
            self.conn.SendNote(n)

    def _setup_ui(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)
        self.lbl_ip_port = Label(self.window, text=f"Your IP:Port - {self.local_ip}:{self.local_port}")
        self.lbl_ip_port.pack(side=TOP)
        self.remote_ip_entry = Entry(self.window, bd=5)
        self.remote_ip_entry.pack(side=LEFT)
        self.remote_port_entry = Entry(self.window, bd=5)
        self.remote_port_entry.pack(side=LEFT)
        connect_button = Button(self.window, text="Connect", command=self.set_remote_details)
        connect_button.pack(side=LEFT)

    def set_remote_details(self):
        self.remote_ip = self.remote_ip_entry.get()
        self.remote_port = int(self.remote_port_entry.get())
        self.connect_to_peer()

if __name__ == '__main__':
    root = Tk()
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    local_ip = get_local_ip()
    local_port = 11912 
    username = None
    while username is None:
        username = simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()
    c = Client(username, frame, local_ip, local_port)