# main.py
import tkinter as tk
from tkinter import messagebox
import time
import sys
import os
from Homepage.homepage import HomePage
from Temporary.temp import TestPage

from Login.auth_ui import AuthWindow

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

class PostureTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Posture Pomodoro Timer")
        self.root.geometry("500x600")
        self.root.configure(bg='#2E3440')
        
        # Timer variables
        self.work_time = 50 * 60  # 50 minutes in seconds
        self.break_time = 10 * 60  # 10 minutes break
        self.time_remaining = self.work_time
        self.is_working = True
        self.is_running = False
        self.start_time = None
        
        # Posture state (0-4, with 4 being the worst posture)
        self.posture_state = 0
        
        # Create GUI elements
        self.create_widgets()
        
        # Start the timer update loop
        self.update_timer()
    
    def create_widgets(self):
        # Main title
        title_label = tk.Label(
            self.root, 
            text="Posture Pomodoro Timer", 
            font=("Arial", 20, "bold"),
            fg='#D8DEE9',
            bg='#2E3440'
        )
        title_label.pack(pady=20)
        
        # Timer display
        self.timer_label = tk.Label(
            self.root,
            text="50:00",
            font=("Arial", 36, "bold"),
            fg='#88C0D0',
            bg='#2E3440'
        )
        self.timer_label.pack(pady=10)
        
        # Avatar canvas
        self.avatar_canvas = tk.Canvas(
            self.root,
            width=300,
            height=300,
            bg='#3B4252',
            highlightthickness=0
        )
        self.avatar_canvas.pack(pady=20)
        
        # Draw the initial avatar
        self.draw_avatar()
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg='#2E3440')
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            button_frame,
            text="Start",
            command=self.start_timer,
            font=("Arial", 14),
            bg='#A3BE8C',
            fg='#2E3440',
            width=10
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_timer,
            font=("Arial", 14),
            bg='#EBCB8B',
            fg='#2E3440',
            width=10
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to work!",
            font=("Arial", 14),
            fg='#D8DEE9',
            bg='#2E3440'
        )
        self.status_label.pack(pady=10)
    
    def draw_avatar(self):
        self.avatar_canvas.delete("all")
        
        # Base coordinates
        center_x = 150
        head_y = 100
        neck_length = 30 + (self.posture_state * 10)
        shoulder_y = head_y + neck_length
        back_curve = self.posture_state * 15
        
        # Draw head
        self.avatar_canvas.create_oval(
            center_x - 30, head_y - 30,
            center_x + 30, head_y + 30,
            fill='#E5E9F0', outline='#D8DEE9', width=2
        )
        
        # Draw eyes
        self.avatar_canvas.create_oval(
            center_x - 15, head_y - 10,
            center_x - 5, head_y,
            fill='#2E3440'
        )
        self.avatar_canvas.create_oval(
            center_x + 5, head_y - 10,
            center_x + 15, head_y,
            fill='#2E3440'
        )
        
        # Draw mouth (changes with posture state)
        mouth_y = head_y + 15
        mouth_expression = "😐" if self.posture_state < 3 else "😫"
        self.avatar_canvas.create_text(
            center_x, mouth_y,
            text=mouth_expression,
            font=("Arial", 16)
        )
        
        # Draw neck
        self.avatar_canvas.create_line(
            center_x, head_y + 30,
            center_x, shoulder_y,
            fill='#E5E9F0', width=8
        )
        
        # Draw shoulders
        self.avatar_canvas.create_line(
            center_x - 50, shoulder_y,
            center_x + 50, shoulder_y,
            fill='#E5E9F0', width=20
        )
        
        # Draw back (curves based on posture state)
        self.avatar_canvas.create_line(
            center_x, shoulder_y,
            center_x - back_curve, shoulder_y + 100,
            fill='#E5E9F0', width=12
        )
        
        # Draw chair
        chair_y = shoulder_y + 120
        self.avatar_canvas.create_rectangle(
            center_x - 70, chair_y,
            center_x + 70, chair_y + 20,
            fill='#5E81AC', outline='#81A1C1'
        )
        
        # Draw desk
        desk_y = shoulder_y + 40
        self.avatar_canvas.create_rectangle(
            center_x - 100, desk_y,
            center_x + 100, desk_y + 10,
            fill='#5E81AC', outline='#81A1C1'
        )
        
        # Draw computer
        screen_height = 40
        self.avatar_canvas.create_rectangle(
            center_x - 30, desk_y - screen_height,
            center_x + 30, desk_y,
            fill='#BF616A', outline='#D08770'
        )
        
        # Draw posture state indicator
        posture_text = f"Posture: {'Good' if self.posture_state == 0 else 'Fair' if self.posture_state < 3 else 'Poor'}"
        self.avatar_canvas.create_text(
            center_x, 20,
            text=posture_text,
            font=("Arial", 12, "bold"),
            fill='#D8DEE9'
        )
    
    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            self.start_button.config(text="Pause")
        else:
            self.is_running = False
            self.start_button.config(text="Resume")
    
    def reset_timer(self):
        self.is_running = False
        self.is_working = True
        self.time_remaining = self.work_time
        self.posture_state = 0
        self.start_button.config(text="Start")
        self.status_label.config(text="Ready to work!")
        self.update_timer_display()
        self.draw_avatar()
    
    def update_timer(self):
        if self.is_running:
            elapsed = time.time() - self.start_time
            self.time_remaining -= elapsed
            
            # Update posture based on work time elapsed
            if self.is_working:
                work_progress = 1 - (self.time_remaining / self.work_time)
                self.posture_state = min(4, int(work_progress * 5))
                self.draw_avatar()
            
            if self.time_remaining <= 0:
                self.is_running = False
                if self.is_working:
                    # Work period ended, start break
                    self.is_working = False
                    self.time_remaining = self.break_time
                    self.show_break_message()
                    self.posture_state = 0  # Reset posture after break
                else:
                    # Break ended, start work period
                    self.is_working = True
                    self.time_remaining = self.work_time
                
                self.draw_avatar()
                self.start_time = time.time()
                self.is_running = True
            
            self.start_time = time.time()
        
        self.update_timer_display()
        self.root.after(1000, self.update_timer)
    
    def update_timer_display(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        timer_text = f"{int(minutes):02d}:{int(seconds):02d}"
        mode_text = "Work Mode" if self.is_working else "Break Time!"
        
        self.timer_label.config(text=timer_text)
        self.status_label.config(text=mode_text)
    
    def show_break_message(self):
        break_tasks = [
            "1. Correct your posture",
            "2. Stand up and walk around",
            "3. Look away from the screen for 20 seconds",
            "4. Stretch your arms and shoulders",
            "5. Take deep breaths for relaxation"
        ]
        
        message = "Time for a break!\n\nPlease do the following:\n\n" + "\n".join(break_tasks)
        messagebox.showinfo("Break Time!", message)


def main() -> None:
    root = tk.Tk()
    app = PostureTimer(root)
    # Link to the Profile panel + window.
    try:
        from Profile.profile import attach_profile
    except ImportError:
        # Fallback if running file directly (not via -m)
        import sys, os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from Profile.profile import attach_profile
    attach_profile(root, app, title_prefix="Posture Pomodoro Timer")
    root.mainloop()

if __name__ == "__main__":
    main()

