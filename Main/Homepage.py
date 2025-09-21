#Homepage Python file. Has buttons that leads to all components/features of this application.

import tkinter as tk
from tkinter import ttk

class HomePage:
    #Initialisation
    def __init__(self, root):
        #Config
        self.window_size = "400x400"
        root.resizable(False, False)


        #Root Config
        root.title("Home")
        root.geometry(self.window_size)

        self.main_body_frame = tk.Frame(root)
        self.main_body_frame.grid(row=0, column=0, sticky="nsew")

        #bg = tk.PhotoImage(file = "Homepage/background.png")
        #background_image = tk.Label(main_body_frame, image=bg)
        #background_image.grid(row=0, column=0, sticky="nsew")

        # Load the PNG (must be in same folder as script OR give full path)
        self.bg = tk.PhotoImage(file="Homepage/background.png")

        # Create a label with the image
        self.label = tk.Label(self.main_body_frame, image=self.bg)
        self.label.grid(row=0, column=0)

        self.menu_button = ttk.Button(self.main_body_frame, text="Placeholder", command=self.toggle_menu)
        self.menu_button.grid(row=0, column=0)

    def toggle_menu(self):
        print("toggled")

        # Create frames the first time if they don't exist
        if not hasattr(self, "menu_buttons_frame_left"):
            self.menu_buttons_frame_left = tk.Frame(self.main_body_frame, background='')
            self.menu_buttons_frame_right = tk.Frame(self.main_body_frame, background='')

            # Settings
            menu_left_padding = 40
            menu_right_padding = 40
            button_y_padding = 20

            # Left menu
            self.menu_buttons_frame_left.grid(row=0, column=0, sticky="w", padx=menu_left_padding)

            posture_timer_button = tk.Button(self.menu_buttons_frame_left, text="Posture Timer")
            posture_timer_button.grid(row=0, column=0, sticky="ew", pady=button_y_padding)

            walk_timer_button = tk.Button(self.menu_buttons_frame_left, text="Walk Timer")
            walk_timer_button.grid(row=1, column=0, sticky="ew", pady=button_y_padding)

            work_timer_button = tk.Button(self.menu_buttons_frame_left, text="Work Timer")
            work_timer_button.grid(row=2, column=0, sticky="ew", pady=button_y_padding)

            # Right menu
            self.menu_buttons_frame_right.grid(row=0, column=0, sticky="e", padx=menu_right_padding)

            friends_page_button = tk.Button(self.menu_buttons_frame_right, text="Friends Page")
            friends_page_button.grid(row=0, column=0, sticky="ew", pady=button_y_padding)

            shower_button = tk.Button(self.menu_buttons_frame_right, text="Shower")
            shower_button.grid(row=1, column=0, sticky="ew", pady=button_y_padding)

            work_timer_button = tk.Button(self.menu_buttons_frame_right, text="Work Timer")
            work_timer_button.grid(row=2, column=0, sticky="ew", pady=button_y_padding)

        else:
            # Toggle visibility
            if self.menu_buttons_frame_left.winfo_ismapped():
                self.menu_buttons_frame_left.grid_forget()
                self.menu_buttons_frame_right.grid_forget()
            else:
                self.menu_buttons_frame_left.grid(row=0, column=0, sticky="w", padx=40)
                self.menu_buttons_frame_right.grid(row=0, column=0, sticky="e", padx=40)
        


if __name__ == "__main__":
    root = tk.Tk()
    
    home_page = HomePage(root)
    root.mainloop()

#hi
