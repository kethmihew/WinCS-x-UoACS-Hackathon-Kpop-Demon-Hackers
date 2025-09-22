# homepage.py
import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Main Frame 
        self.main_body_frame = tk.Frame(self)
        self.main_body_frame.grid(row=0, column=0, sticky="nsew")

        # Background Image
        self.bg = tk.PhotoImage(file="Homepage/background.png").zoom(2, 2)

        self.canvas = tk.Canvas(
            self.main_body_frame,
            width=self.bg.width(),
            height=self.bg.height(),
            highlightthickness=0,  # remove border
            bd=0
        )
        self.canvas.grid(row=0, column=0)

        # Center background on canvas
        self.canvas.create_image(
            self.bg.width() // 2, self.bg.height() // 2,
            image=self.bg, anchor="center"
        )

        # Animated Sprite
        self.frames = [
            tk.PhotoImage(file=f"Homepage/sprites/sprite{i}.png")
            for i in range(1, 5)
        ]
        self.canvas.image_refs = self.frames  # prevent garbage collection

        # Place sprite in the center of the canvas
        sprite_x = self.bg.width() // 2
        sprite_y = self.bg.height() // 2
        self.sprite = self.canvas.create_image(sprite_x, sprite_y, image=self.frames[0], anchor="center")

        self.sprite = self.canvas.create_image(
            sprite_x, sprite_y, 
            image=self.frames[0], 
            anchor="center"
        )

        # Bind a click event to the sprite
        self.canvas.tag_bind(self.sprite, "<Button-1>", lambda e: self.toggle_menu())

        # Animation state
        self.frame_index = 0
        self.animate()

        # Menu Setup (hidden initially)
        self.menu_buttons_frame_left = tk.Frame(self.main_body_frame, background="")
        self.menu_buttons_frame_right = tk.Frame(self.main_body_frame, background="")

        self.button_width = 20
        self.button_height = 2

        # Left menu buttons
        self.posture_timer_button = tk.Button(self.menu_buttons_frame_left, text="Posture Timer", width=self.button_width, height=self.button_height)
        self.walk_timer_button = tk.Button(self.menu_buttons_frame_left, text="Walk Timer", width=self.button_width, height=self.button_height)
        self.work_timer_button = tk.Button(self.menu_buttons_frame_left, text="Work Timer", width=self.button_width, height=self.button_height)

        # Right menu buttons
        self.friends_page_button = tk.Button(self.menu_buttons_frame_right, text="Friends Page", width=self.button_width, height=self.button_height)
        self.shower_button = tk.Button(self.menu_buttons_frame_right, text="Shower", width=self.button_width, height=self.button_height)
        self.login_button = tk.Button(self.menu_buttons_frame_right, text="Login", width=self.button_width, height=self.button_height)

        # Toggle state
        self.menu_visible = False

        # Menu Layout Settings
        self.menu_x_padding = 80
        self.button_y_padding = 20

    def toggle_menu(self):
        if self.menu_visible:
            self.menu_buttons_frame_left.grid_forget()
            self.menu_buttons_frame_right.grid_forget()
            self.menu_visible = False
        else:
            # Left menu
            self.menu_buttons_frame_left.grid(row=0, column=0, sticky="w", padx=self.menu_x_padding)
            self.posture_timer_button.grid(row=0, column=0, sticky="ew", pady=self.button_y_padding)
            self.walk_timer_button.grid(row=1, column=0, sticky="ew", pady=self.button_y_padding)
            self.work_timer_button.grid(row=2, column=0, sticky="ew", pady=self.button_y_padding)

            # Right menu
            self.menu_buttons_frame_right.grid(row=0, column=0, sticky="e", padx=self.menu_x_padding)
            self.friends_page_button.grid(row=0, column=0, sticky="ew", pady=self.button_y_padding)
            self.shower_button.grid(row=1, column=0, sticky="ew", pady=self.button_y_padding)
            self.login_button.grid(row=2, column=0, sticky="ew", pady=self.button_y_padding)

            self.menu_visible = True

    def animate(self):
        """Cycle through sprite frames for animation"""
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.canvas.itemconfig(self.sprite, image=self.frames[self.frame_index])
        self.after(150, self.animate)  # call again after 150ms


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Home")
    root.geometry("400x400")
    root.resizable(False, False)

    home_page = HomePage(root, None)
    home_page.pack(fill="both", expand=True)

    root.mainloop()
