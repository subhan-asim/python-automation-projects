import os.path
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import tkinter as tk
from tkinter import filedialog
import threading
import csv

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = None

# Authenticate
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', "w") as token:
        token.write(creds.to_json())
service = build('calendar', 'v3', credentials=creds)

# Global filepath variable
filepath = None

# GUI
root = tk.Tk()
root.title("Auto Day Scheduler")
root.geometry("800x600")

def upload_csv():
    global filepath
    file = filedialog.askopenfile(
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv")]
    )
    if file:
        filepath = file.name
        status_label.config(text=f"Selected file: {filepath}")

def add_events_thread():
    send_btn.config(state=tk.DISABLED)
    try:
        with open(filepath, "r", encoding='utf-16' ,newline='') as f:
            reader = csv.reader(f)
            lines = list(reader)

        start_dt = datetime.now() + timedelta(minutes=20)

        for row in lines[1:]:
            if len(row) != 2:
                print(f"Skipping bad row {row}")
                continue
            task, time = row
            summary = task.strip()
            try:
                duration = int(time.strip())
            except ValueError:
                print(f"Skipping bad duration: {time.strip()} in row: {row}")
            end_dt = start_dt + timedelta(minutes=duration)

            status_label.config(text=f"Creating: {summary} from {start_dt.strftime('%H:%M')} to {end_dt.strftime('%H:%M')}")

            event = {
                'summary': summary,
                'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Asia/Karachi'},
                'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Asia/Karachi'}
            }

            service.events().insert(calendarId='primary', body=event).execute()
            start_dt = end_dt + timedelta(minutes=20)

        status_label.config(text=f"Added {len(lines)-1} events to your schedule.")
    except Exception as e:
        status_label.config(text=f"Error: {e}")
    finally:
        send_btn.config(state=tk.NORMAL)

def add_events():
    if not filepath:
        status_label.config(text="Please select a CSV file first.")
        return
    threading.Thread(target=add_events_thread).start()

# UI Layout
tk.Label(root, text="Select CSV file").pack(pady=10)
upload_Btn = tk.Button(root, text="Upload", command=upload_csv)
upload_Btn.pack(pady=5)

tk.Label(root, text="Add Events to your schedule: ").pack(pady=5)
send_btn = tk.Button(root, text="Add Events", command=add_events)
send_btn.pack(pady=5)

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

root.mainloop()