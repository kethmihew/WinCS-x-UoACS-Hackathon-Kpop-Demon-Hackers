# Make copies/copy the code when making a new page. Essential lines are marked.
# Once you have created the page, let me know @rhbi-auk so I can update main.py. I have added steps on there if you wish to add it yourself.

import tkinter as tk # ------ ESSENTIAL STARTS HERE 

class NewFeature(tk.Frame): # Change 'NewFeature' to the name of the page. e.g. HomePage
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller # ------ ESSENTIAL ENDS HERE 

        label = tk.Label(self, text="This is the New Feature Page") # EXAMPLE TEXT
        label.pack(pady=20)

        back_button = tk.Button( # Example button 
            self,
            text="Back to Home",
            command=lambda: controller.show_frame("HomePage")
        )
        back_button.pack(pady=10)