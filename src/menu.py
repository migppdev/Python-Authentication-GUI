import tkinter as tk

class App(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"Tu contenido, {username}")
        self.geometry("500x500")



if __name__ == '__main__':
    app = App()
    app.mainloop()