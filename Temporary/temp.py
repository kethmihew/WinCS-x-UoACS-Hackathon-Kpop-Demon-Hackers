# homepage.py
import tkinter as tk

class TestPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)   # HomePage is just a frame
        self.controller = controller

        # Main body frame
        self.main_body_frame = tk.Frame(self)
        self.main_body_frame.grid(row=0, column=0, sticky="nsew")

        self.TestLabel = tk.Label(self, text="Hello world")
        self.TestLabel.grid(row=0, column=0)

        self.test_button = tk.Button(self, text="CLICK ME!!!", command=lambda: controller.show_frame("HomePage"))
        self.test_button.grid(row=0, column=0)