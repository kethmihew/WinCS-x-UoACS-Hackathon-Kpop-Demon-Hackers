# homepage.py
import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.main_body_frame = tk.Frame(self)
        self.main_body_frame.grid(row=0, column=0, sticky="nsew")

        self.bg = tk.PhotoImage(file="Main/Homepage/background.png")
        self.label = tk.Label(self.main_body_frame, image=self.bg)
        self.label.grid(row=0, column=0)

        # Menus (created immediately, but hidden)
        self.menu_buttons_frame_left = tk.Frame(self.main_body_frame, background='')
        self.menu_buttons_frame_right = tk.Frame(self.main_body_frame, background='')

        # Left menu buttons
        self.posture_timer_button = tk.Button(self.menu_buttons_frame_left, text="Posture Timer")
        self.walk_timer_button = tk.Button(self.menu_buttons_frame_left, text="Walk Timer")
        self.work_timer_button = tk.Button(self.menu_buttons_frame_left, text="Work Timer")

        # Right menu buttons
        self.friends_page_button = tk.Button(self.menu_buttons_frame_right, text="Friends Page")
        self.shower_button = tk.Button(self.menu_buttons_frame_right, text="Shower")
        self.work_timer_button_right = tk.Button(self.menu_buttons_frame_right, text="Work Timer")

        # Initially hidden
        self.menu_visible = False

    def toggle_menu(self):
        # Define padding values (you can move these to __init__ if you want them app-wide)
        menu_x_padding = 20   # left/right padding
        button_y_padding = 20 # vertical spacing between buttons

        if self.menu_visible:
            self.menu_buttons_frame_left.grid_forget()
            self.menu_buttons_frame_right.grid_forget()
            self.menu_visible = False
        else:
            # Place frames + buttons
            self.menu_buttons_frame_left.grid(row=0, column=0, sticky="w", padx=menu_x_padding)
            self.posture_timer_button.grid(row=0, column=0, sticky="ew", pady=button_y_padding)
            self.walk_timer_button.grid(row=1, column=0, sticky="ew", pady=button_y_padding)
            self.work_timer_button.grid(row=2, column=0, sticky="ew", pady=button_y_padding)

            self.menu_buttons_frame_right.grid(row=0, column=0, sticky="e", padx=menu_x_padding)
            self.friends_page_button.grid(row=0, column=0, sticky="ew", pady=button_y_padding)
            self.shower_button.grid(row=1, column=0, sticky="ew", pady=button_y_padding)
            self.work_timer_button_right.grid(row=2, column=0, sticky="ew", pady=button_y_padding)

            self.menu_visible = True

