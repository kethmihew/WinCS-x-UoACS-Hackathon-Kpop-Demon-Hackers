# main.py
import tkinter as tk
from Homepage.homepage import HomePage
from Temporary.temp import TestPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test App")
        self.geometry("320x320")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Register all pages
        for PageClass in (HomePage, TestPage):  # add more pages later
            frame = PageClass(parent=container, controller=self)
            self.frames[PageClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

        #Main Menu Button
        home_page = self.frames["HomePage"]
        menu_button = tk.Button(home_page.main_body_frame, text="Toggle Menu",
                                command=home_page.toggle_menu)
        menu_button.grid(row=0, column=0)

        #Configuration and set-up of menu buttons
        home_page.friends_page_button.config(
            command=lambda: (home_page.toggle_menu(), self.show_frame("TestPage"))
        )

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
