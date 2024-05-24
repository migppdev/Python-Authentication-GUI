import tkinter as tk
from auth_db import verify_user, register_user, close_db
from tkinter import messagebox
from main import App as app_nueva_ventana

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro")
        self.geometry("500x600")
        self.resizable(0, 0)
        self.config(background="#E0FBE2")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        tk.Label(self, text="Usuario", font=("Ubuntu", 11), background="#E0FBE2").grid(row=0, column=0)
        self.username = tk.Entry(self, font=("Ubuntu", 11))
        self.username.grid(row=0, column=1)

        tk.Label(self, text="Contraseña", font=("Ubuntu", 11), background="#E0FBE2").grid(row=1, column=0)
        self.password = tk.Entry(self, font=("Ubuntu", 11), show="*")
        self.password.grid(row=1, column=1)

        self.send_btn = tk.Button(self, text="Registrarse", font=("Ubuntu", 11), command=self.register_user_gui, background="#B0EBB4", highlightbackground="#000000")
        self.send_btn.grid(row=2, columnspan=2)

        self.change_mode_lbl = tk.Label(self, foreground="blue", font=("Ubuntu", 9, "underline"), text="¿Ya estas registrado? Iniciar sesión", background="#E0FBE2")
        self.change_mode_lbl.grid(row=3, columnspan=2, sticky="N")

        self.change_mode_lbl.bind("<Button-1>", self.show_log_in_gui)
        
    def register_user_gui(self, event=None):
        username = self.username.get()
        password = self.password.get()
        try:
            if all([len(x) > 3 for x in [username, password]]):
                if register_user(username, password):
                    messagebox.showinfo(title="Éxito", message=f"Usuario {username} creado con éxito")
                elif register_user(username, password) is False:
                    messagebox.showerror(title="Error", message=f"El usuario {username} ya existe")
                else:
                    messagebox.showerror(title="Error", message="La base de datos no estaba creada, intentelo de nuevo")
            else:
                messagebox.showerror(title="Error", message="Usuario u contraseña muy cortos")
        finally:
            self.show_log_in_gui()

    def log_in_user_gui(self, event=None):
        username = self.username.get()
        password = self.password.get()
        if verify_user(username, password):
            self.log_in_redirect(username=username)
        else:
            messagebox.showerror(title="Inicio de sesion fallido", message="Revise los campos")

    def log_in_redirect(self, username):
        self.on_closing()
        app = app_nueva_ventana(username)
        app.mainloop()


    def show_log_in_gui(self, event=None):
        self.title("Iniciar sesión")
        self.username.focus_set()
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.send_btn.config(text="Iniciar sesión")
        self.change_mode_lbl.config(text="¿No tiene cuenta? Registrarse")
        self.send_btn.config(command=self.log_in_user_gui)
        self.change_mode_lbl.bind("<Button-1>", self.show_sign_in_gui)
    
    def show_sign_in_gui(self, event=None):
        self.title("Registro")
        self.username.focus_set()
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.send_btn.config(text="Registrarse")
        self.change_mode_lbl.config(text="¿Ya estas registrado? Iniciar sesión")
        self.send_btn.config(command=self.log_in_user_gui)
        self.change_mode_lbl.bind("<Button-1>", self.show_log_in_gui)

    def on_closing(self):
        close_db()
        self.destroy()

    

if __name__ == '__main__':
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
