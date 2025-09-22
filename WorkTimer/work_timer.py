# work_timer.py
import tkinter as tk
from tkinter import messagebox
import time
import os

class WorkTimer(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#F5F5DC')
        self.controller = controller

        # ---- Profile mini-panel + Edit window (non-invasive) ----
        try:
            from Profile.profile import attach_profile
        except ImportError:
            import sys, os
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            from Profile.profile import attach_profile

        # Attach profile to the *root window* (controller is your MainApp)
        root = self.controller.winfo_toplevel()
        attach_profile(root, self, title_prefix="Posture Pomodoro Timer")


        # Timer variables
        self.original_work_time = 50 * 60  # 50 minutes
        self.work_time = 50 * 60
        self.break_time = 5 * 60
        self.time_remaining = self.work_time
        self.is_working = True
        self.is_running = False
        self.start_time = None

        # Posture state (0-4)
        self.posture_state = 0

        # Load images
        self.posture_images = []
        self.computer_image = None
        self.load_images()

        # Create GUI elements
        self.create_widgets()

        # Start the timer update loop
        self.update_timer()

    def load_images(self):
        try:
            image_dir = "WorkTimer"
            for i in range(1, 5):
                image_path = os.path.join(image_dir, f"posture{i}.png")
                if os.path.exists(image_path):
                    img = tk.PhotoImage(file=image_path).zoom(4, 4)
                    self.posture_images.append(img)
                else:
                    print(f"Image not found: {image_path}")
                    self.posture_images = None
                    break

            computer_path = os.path.join(image_dir, "computer-removebg-preview.png")
            if os.path.exists(computer_path):
                self.computer_image = tk.PhotoImage(file=computer_path).subsample(2, 2)
            else:
                print(f"Image not found: {computer_path}")
                self.computer_image = None

        except Exception as e:
            print(f"Error loading images: {e}")
            self.posture_images = None
            self.computer_image = None

    def create_widgets(self):
        title_label = tk.Label(
            self,
            text="Work Timer",
            font=("Arial", 24, "bold"),
            fg='#4B3621',
            bg='#F5F5DC'
        )
        title_label.pack(pady=10)

        self.timer_label = tk.Label(
            self,
            text="50:00",
            font=("Arial", 48, "bold"),
            fg='#8B4513',
            bg='#F5F5DC'
        )
        self.timer_label.pack(pady=5)

        self.status_label = tk.Label(
            self,
            text="Work Mode",
            font=("Arial", 14),
            fg='#4B3621',
            bg='#F5F5DC'
        )
        self.status_label.pack(pady=5)

        button_frame = tk.Frame(self, bg='#F5F5DC')
        button_frame.pack(pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="Start",
            command=self.start_timer,
            font=("Arial", 14),
            bg='#A3BE8C',
            fg='#4B3621',
            width=10,
            relief=tk.RAISED,
            bd=2
        )
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_timer,
            font=("Arial", 14),
            bg='#EBCB8B',
            fg='#4B3621',
            width=10,
            relief=tk.RAISED,
            bd=2
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)

        adjust_frame = tk.Frame(self, bg='#F5F5DC')
        adjust_frame.pack(pady=10)

        self.decrease_button = tk.Button(
            adjust_frame,
            text="-60s",
            command=self.decrease_time,
            font=("Arial", 12),
            bg='#D2B48C',
            fg='#4B3621',
            width=6,
            height=1,
            relief=tk.RAISED,
            bd=2
        )
        self.decrease_button.pack(side=tk.LEFT, padx=5)

        self.increase_button = tk.Button(
            adjust_frame,
            text="+60s",
            command=self.increase_time,
            font=("Arial", 12),
            bg='#D2B48C',
            fg='#4B3621',
            width=6,
            height=1,
            relief=tk.RAISED,
            bd=2
        )
        self.increase_button.pack(side=tk.LEFT, padx=5)

        content_frame = tk.Frame(self, bg='#F5F5DC')
        content_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            content_frame,
            width=600,
            height=350,
            bg='#F5F5DC',
            highlightthickness=0
        )
        self.canvas.pack()

        self.home_button = tk.Button(
            button_frame,
            text="Home",
            command=lambda: self.controller.show_frame("HomePage"),
            font=("Arial", 14),
            bg='#EBCB8B',
            fg='#4B3621',
            width=10,
            relief=tk.RAISED,
            bd=2
        )

        self.home_button.pack(side=tk.LEFT, padx=10)

        self.draw_scene()

    def draw_scene(self):
        self.canvas.delete("all")
        canvas_center_x = 300
        canvas_center_y = 175

        if self.posture_images and len(self.posture_images) >= 4:
            avatar_x = canvas_center_x + 15
            avatar_y = canvas_center_y + 20
            img_index = min(self.posture_state, 3)
            self.canvas.create_image(avatar_x, avatar_y, image=self.posture_images[img_index], anchor=tk.CENTER)
        else:
            self.draw_avatar_fallback(canvas_center_x - 120, canvas_center_y + 20)

        if self.computer_image:
            comp_x = canvas_center_x + 120
            comp_y = canvas_center_y + 20
            self.canvas.create_image(comp_x, comp_y, image=self.computer_image, anchor=tk.CENTER)
        else:
            comp_width = 100
            comp_height = 70
            comp_x = canvas_center_x + 120 - comp_width/2
            comp_y = canvas_center_y + 20 - comp_height/2
            self.canvas.create_rectangle(
                comp_x, comp_y, comp_x + comp_width, comp_y + comp_height,
                fill='#2F4F4F', outline='#2F4F4F', width=2
            )

    def draw_avatar_fallback(self, x, y):
        head_y = y - 40
        neck_length = 20 + (self.posture_state * 8)
        shoulder_y = head_y + neck_length
        back_curve = self.posture_state * 12

        self.canvas.create_oval(
            x - 25, head_y - 25, x + 25, head_y + 25,
            fill='#FFEBCD', outline='#DEB887', width=2
        )
        self.canvas.create_oval(x + 5, head_y - 10, x + 15, head_y, fill='#4B3621')

        mouth_y = head_y + 10
        if self.posture_state < 3:
            self.canvas.create_line(x - 5, mouth_y, x + 5, mouth_y, fill='#4B3621', width=2)
        else:
            self.canvas.create_arc(x - 5, mouth_y - 3, x + 5, mouth_y + 3,
                                   start=0, extent=-180, fill='', outline='#4B3621', width=2)

        self.canvas.create_line(x, head_y + 25, x, shoulder_y, fill='#FFEBCD', width=6)
        self.canvas.create_line(x - 30, shoulder_y, x + 30, shoulder_y, fill='#FFEBCD', width=16)
        self.canvas.create_line(x, shoulder_y, x - back_curve, shoulder_y + 80, fill='#FFEBCD', width=10)

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            self.start_button.config(text="Pause")
            self.status_label.config(text="Work Mode")
        else:
            self.is_running = False
            self.start_button.config(text="Resume")
            mode = "Work" if self.is_working else "Break"
            self.status_label.config(text=f"{mode} Mode")

    def reset_timer(self):
        self.is_running = False
        self.is_working = True
        self.work_time = self.original_work_time
        self.time_remaining = self.work_time
        self.posture_state = 0
        self.start_button.config(text="Start")
        self.status_label.config(text="Work Mode")
        self.update_timer_display()
        self.draw_scene()

    def update_timer(self):
        if self.is_running:
            elapsed = time.time() - self.start_time
            self.time_remaining -= elapsed
            self.update_posture_state()

            if self.time_remaining <= 0:
                self.is_running = False
                if self.is_working:
                    self.is_working = False
                    self.time_remaining = self.break_time
                    self.show_break_message()
                    self.posture_state = 0
                    self.status_label.config(text="Break Mode")
                else:
                    self.is_working = True
                    self.work_time = self.original_work_time
                    self.time_remaining = self.work_time
                    self.show_work_message()
                    self.status_label.config(text="Work Mode")
                self.draw_scene()
                self.start_time = time.time()
                self.is_running = True

            self.start_time = time.time()
            self.update_timer_display()

        self.after(1000, self.update_timer)

    def update_timer_display(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        timer_text = f"{int(minutes):02d}:{int(seconds):02d}"
        self.timer_label.config(text=timer_text)
        self.draw_scene()

    def decrease_time(self):
        self.time_remaining -= 60
        if self.time_remaining < 0:
            self.time_remaining = 0
        if self.is_working:
            self.work_time = self.time_remaining
        self.update_posture_state()
        self.update_timer_display()

    def increase_time(self):
        self.time_remaining += 60
        if self.is_working:
            self.work_time = self.time_remaining
        self.update_posture_state()
        self.update_timer_display()

    def update_posture_state(self):
        if self.is_working:
            minutes_remaining = self.time_remaining // 60
            if minutes_remaining >= 41:
                self.posture_state = 0
            elif minutes_remaining >= 31:
                self.posture_state = 1
            elif minutes_remaining >= 21:
                self.posture_state = 2
            elif minutes_remaining >= 11:
                self.posture_state = 3
            else:
                self.posture_state = 4
        else:
            self.posture_state = 0
        self.draw_scene()

    def show_break_message(self):
        break_tasks = [
            "1. Correct your posture",
            "2. Stand up and walk around",
            "3. Look away from your screen",
            "4. Stretch your arms and shoulders"
        ]
        message = "Time for a break!\n\nPlease do the following:\n\n" + "\n".join(break_tasks)
        messagebox.showinfo("Break Time!", message)

    def show_work_message(self):
        messagebox.showinfo("Work Time", "Break is over! Time to get back to work.")

    
