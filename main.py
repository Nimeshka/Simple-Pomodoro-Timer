import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from tkinter import ttk

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("250x130")
        self.root.attributes('-topmost', True)
        self.time_left = 12 * 60  # 12 minutes
        self.running = False
        self.total_time = 0

        # Create SQLite database
        self.conn = sqlite3.connect('pomodoro_timer.db')
        self.create_table()
        
        self.label = tk.Label(root, text="12:00", font=("Helvetica", 24))
        self.label.pack(pady=10)
        
        self.total_label = tk.Label(root, text="Total Time: 0:00", font=("Helvetica", 12))
        self.total_label.pack()
        
        # Create a frame for the buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        
        self.reset_button = tk.Button(button_frame, text="Start", command=self.start_reset_timer)
        self.reset_button.grid(row=0, column=0, padx=5)
        
        self.view_button = tk.Button(button_frame, text="View Total Time", command=self.view_total_time)
        self.view_button.grid(row=0, column=1, padx=5)
        
        self.update_timer()
        
        # Center the window on the screen
        self.center_window()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS time_spent (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time_spent INTEGER
            )
        """)
        self.conn.commit()

    def update_timer(self):
        if self.running:
            mins, secs = divmod(self.time_left, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            self.label.config(text=time_format)
            if self.time_left <= 0:
                self.running = False
                self.reset_button.config(text="Start")
                self.total_time += 12 * 60
                self.update_total_time_label()
                self.show_times_up_message()
            self.time_left -= 1
        self.root.after(1000, self.update_timer)

    def update_total_time_label(self):
        total_hours, remainder = divmod(self.total_time, 3600)
        total_mins = remainder // 60
        self.total_label.config(text=f"Total Time: {total_hours}:{total_mins:02d}")

    def start_reset_timer(self):
        elapsed_time = 12 * 60 - self.time_left
        if elapsed_time > 0:
            self.total_time += elapsed_time
            self.update_total_time_label()
            
            # Save time spent to SQLite
            cursor = self.conn.cursor()
            current_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO time_spent (date, time_spent) VALUES (?, ?)", (current_date, elapsed_time))
            self.conn.commit()
        
        self.time_left = 12 * 60
        
        if not self.running:
            self.running = True
            self.reset_button.config(text="Reset")
        else:
            self.running = False
            self.reset_button.config(text="Start")

    def view_total_time(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT date, SUM(time_spent) FROM time_spent GROUP BY date")
        results = cursor.fetchall()
        
        # Create a new window to display the total time
        view_window = tk.Toplevel(self.root)
        view_window.title("Total Time Spent")
        view_window.geometry("300x200")
        view_window.attributes('-topmost', True)
        view_window.geometry(f"+{self.root.winfo_x()}+{self.root.winfo_y()}")
        
        tree = ttk.Treeview(view_window, columns=("Date", "Total Time"), show='headings')
        tree.heading("Date", text="Date")
        tree.heading("Total Time", text="Total Time (hours:minutes)")
        
        for row in results:
            total_hours, remainder = divmod(row[1], 3600)
            total_mins = remainder // 60
            tree.insert('', 'end', values=(row[0], f"{total_hours}:{total_mins:02d}"))
        
        tree.pack(fill=tk.BOTH, expand=True)

    def show_times_up_message(self):
        self.root.attributes('-topmost', True)
        messagebox.showinfo("Time's up!", "Time for a break!")
        self.root.attributes('-topmost', True)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
