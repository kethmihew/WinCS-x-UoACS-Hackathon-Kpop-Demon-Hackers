# ---- IMPORTANT: To anyone wishing to add their page: Please follow the steps in the comments below. ----

# main.py
import tkinter as tk

#STEP 1: IMPORT YOUR PAGE HERE. e.g. from FolderName.python_file import ClassName
from Homepage.homepage import HomePage
from Temporary.temp import TestPage
from WorkTimer.work_timer import WorkTimer

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test App")
        self.geometry("640x640")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # STEP 2: INSERT ClassName OF YOUR PAGE. 
        for PageClass in (HomePage, TestPage, WorkTimer): # ADD INSIDE OF BRACKETS HERE.
            frame = PageClass(parent=container, controller=self)
            self.frames[PageClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

        # Main Menu Button
        home_page = self.frames["HomePage"]

        # STEP 3 (FINAL STEP): USE THIS TEMPLATE TO CONFIGURE THE RESPECTIVE BUTTON FROM homepage.py
        # CHANGE 'example_page' to the name of the page button. You can find all the buttons in homepage.py
        # CHANGE 'ClassName' WITH NAME OF CLASS
        """
            home_page.[example_page_button].config(
            command=lambda: (home_page.toggle_menu(), self.show_frame("ClassName"))
        )
        """
        home_page.friends_page_button.config(
            command=lambda: (home_page.toggle_menu(), self.show_frame("TestPage"))
        )

        home_page.work_timer_button.config(command=lambda: [self.show_frame("WorkTimer"),
                                               home_page.toggle_menu()])
        

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
