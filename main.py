import tkinter as tk
from tkinter import messagebox
import time

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("200x150")
        self.root.attributes('-topmost', True)
        self.time_left = 12 * 60  # 12 minutes
        self.running = False
        self.total_time = 0
        
        self.label = tk.Label(root, text="12:00", font=("Helvetica", 24))
        self.label.pack(pady=10)
        
        self.total_label = tk.Label(root, text="Total Time: 0:00", font=("Helvetica", 12))
        self.total_label.pack()
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(pady=10)
        
        self.update_timer()

    def update_timer(self):
        if self.running:
            mins, secs = divmod(self.time_left, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            self.label.config(text=time_format)
            if self.time_left <= 0:
                self.running = False
                self.total_time += 12 * 60
                total_mins, total_secs = divmod(self.total_time, 60)
                self.total_label.config(text=f"Total Time: {total_mins}:{total_secs:02d}")
                messagebox.showinfo("Time's up!", "Time for a break!")
            self.time_left -= 1
        self.root.after(1000, self.update_timer)
    
    def reset_timer(self):
        self.total_time += (12 * 60 - self.time_left)
        total_mins, total_secs = divmod(self.total_time, 60)
        self.total_label.config(text=f"Total Time: {total_mins}:{total_secs:02d}")
        self.time_left = 12 * 60
        self.running = True

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
