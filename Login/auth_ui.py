import tkinter as tk
from tkinter import messagebox
from Login import services

class AuthWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.withdraw()

        self.auth_window = tk.Toplevel(self.root)
        self.auth_window.title("Login")
        self.auth_window.geometry("320x320")
        self.auth_window.resizable(False, False)
        self.auth_window.configure(bg="#ffffff")

        self.current_frame = None
        self.show_login_frame()

    def show_login_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.auth_window, bg="#ffffff")
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = (tk.Label(self.current_frame, text="Login", font=("Arial", 12),
                         fg="white", bg="#ffffff"))
        title.pack(anchor="w", pady=(0,20))

        #username
        tk.Label(self.current_frame, text="Username", font=("Arial", 12),
                 fg="white", bg="#ffffff").pack(anchor="w")
        self.login_username_entry = tk.Entry(self.current_frame, font=("Arial", 12), width=30)
        self.login_username_entry.pack(pady=(0, 10))

        tk.Label(self.current_frame, text="Password", font=("Arial", 12),
                 fg="white", bg="#ffffff").pack(anchor="w")
        self.login_password_entry = tk.Entry(self.current_frame, font=("Arial", 12),
                                             width=30, show='*')
        self.login_password_entry.pack(pady=(0, 20))

        #Login Button
        login_button = tk.Button(self.current_frame, text="Login", font=("Arial", 12),
                                 command=self.handle_login, bg="#ffffff", fg="white")
        login_button.pack(pady=(10))

        #Switch to Register
        switch_button = tk.Button(self.current_frame, text="Don't have an account? Register",
                                  font=("Arial", 12), command=self.show_register_frame, bd=0,
                                  bg="#ffffff", fg="white", activebackground='#2E3440', activeforeground='D8DEE9')
        switch_button.pack()

    def show_register_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.auth_window, bg="#2E3440")
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = (tk.Label(self.current_frame, text="Create Account", font=("Arial", 20, "bold"),
                         fg='D8DEE9', bg="#2E3440" ))
        title.pack(anchor="w")

        #Username
        tk.Label(self.current_frame, text="Username", font=("Arial", 20, "bold"),
                 fg='D8DEE9', bg="#2E3440").pack(anchor="w")
        self.register_username_entry = tk.Entry(self.current_frame, font=("Arial", 20), width=30)
        self.register_username_entry.pack(pady=(0, 10))

        #Password
        tk.Label(self.current_frame, text="Password", font=("Arial", 20, "bold"),
                 fg='D8DEE9', bg="#2E3440").pack(anchor="w")
        self.register_password_entry = tk.Entry(self.current_frame, show='*', font=("Arial", 20),
                                                width=30)
        self.register_password_entry.pack(pady=(0, 20))

        #Register Button
        register_button = tk.Button(self.current_frame, text="Register", font=("Arial", 12),
                                    command=self.handle_register, bd=0, bg="#2E3440", fg="#88C0D0")
        register_button.pack(pady=(10))

        #switch to Login page
        switch_button = tk.Button(self.current_frame, text="Already have an account? Login",
                                  command=self.show_login_frame, bd=0, bg="#2E3440", fg="#88C0D0",
                                  activebackground='#2E3440', activeforeground='D8DEE9')
        switch_button.pack()

        def handle_login():
            username = self.register_username_entry.get()
            password = self.register_password_entry.get()

            if services.verify_user(username, password):
                messagebox.showinfo("Success", "Login Successful!")
                self.auth_window.destroy()
                self.on_success()
            else:
                messagebox.showerror("Error", "Login Failed! Invalid useername or password.")

        def handle_register():
            username = self.register_username_entry.get()
            password = self.register_password_entry.get()

            if not services.password_strong(password):
                messagebox.showerror("Error", "Password is weak! It must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit")
                return

            if services.create_user(username, password):
                messagebox.showinfo("Success", "User created successfully!")
                self.show_login_frame()

            else:
                messagebox.showerror("Error", "Username already exists!")
