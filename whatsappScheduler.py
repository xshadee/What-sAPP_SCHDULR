import tkinter as tk
from tkinter import messagebox
import pywhatkit as kit
import schedule
import time
import requests
import random

class WhatsAppSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Message Scheduler")
        
        # Labels and entries for user inputs
        tk.Label(root, text="Phone Number:").grid(row=0, column=0)
        self.phone_entry = tk.Entry(root)
        self.phone_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Query:").grid(row=1, column=0)
        self.query_entry = tk.Entry(root)
        self.query_entry.grid(row=1, column=1)
        
        tk.Label(root, text="Interval (minutes):").grid(row=2, column=0)
        self.interval_entry = tk.Entry(root)
        self.interval_entry.grid(row=2, column=1)
        
        # Button to start the scheduling
        tk.Button(root, text="Start", command=self.start_scheduling).grid(row=3, column=0, columnspan=2)
    
    def start_scheduling(self):
        phone_number = self.phone_entry.get()
        query = self.query_entry.get()
        interval = int(self.interval_entry.get())
        
        if not phone_number or not query or not interval:
            messagebox.showwarning("Input Error", "All fields are required!")
            return
        
        schedule.every(interval).minutes.do(self.job, phone_number, query)
        
        messagebox.showinfo("Scheduler Started", f"Messages will be sent every {interval} minutes.")
        self.run_scheduler()
    
    def job(self, phone_number, query):
        result = self.fetch_poetry(query)
        if result:
            self.send_whatsapp_message(phone_number, result)
    
    def fetch_poetry(self, query):
        response = requests.get(f"https://poetrydb.org/title/{query}")
        if response.status_code == 200:
            poems = response.json()
            if poems and len(poems) > 0:
                poem = random.choice(poems)  # Randomly select a poem
                poem_lines = "\n".join(poem['lines'])  # Join the poem lines into a single string
                return poem_lines
        return "Couldn't find any relevant results for the query."
    
    def send_whatsapp_message(self, phone_number, message):
        # Adjust the timing parameters (hour and minute) as needed
        current_time = time.localtime()
        hour = current_time.tm_hour
        minute = current_time.tm_min + 2  # Send message 2 minutes later
        if minute >= 60:  # Adjust if minutes overflow
            hour += 1
            minute -= 60
        
        # Use sendwhatmsg_instantly instead of sendwhatmsg
        kit.sendwhatmsg_instantly(phone_number, message, wait_time=15)  # Adjust wait_time if necessary
    
    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(5)  # Check every 5 seconds instead of every second

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppSchedulerApp(root)
    root.mainloop()
