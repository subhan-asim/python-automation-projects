import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox
import threading

#Email SENDING

def send_email():
    email = EmailMessage()
    sender = sender_entry.get().strip()
    password = app_password.get()
    recipent = recipent_entry.get().strip()
    subject = subject_entry.get()
    message_content = message_entry.get("1.0", tk.END)
    email['From'] = sender
    email['To'] = recipent
    email['Subject'] = subject
    email.set_content(message_content)
    if not sender or not recipent or not password:
        status_label.config(text="Please make sure all fields are filled.")
        messagebox.showerror("Error", "Please make sure all fields are filled.")
        return
    def send():
        try:
            send_btn.config(state=tk.DISABLED)
            status_label.config(text="Sending eMail...")
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(sender, password)
            smtp.send_message(email)
            smtp.quit()
            status_label.config(text="Mail Sent Successfully.")
        except Exception as e:
            status_label.config(text=e)
            messagebox.showerror("Error", e)
        finally:
            send_btn.config(state=tk.NORMAL)
    threading.Thread(target=send).start()
    

#MAIN GUI
root = tk.Tk()
root.title("Send Email")
root.geometry("800x600")

#INPUT FIELDS
tk.Label(root, text="Sender's Email: ").pack()
sender_entry = tk.Entry(root, width=50)
sender_entry.pack()


tk.Label(root, text="App Password: ").pack()
app_password = tk.Entry(root, width=50, show="*")
app_password.pack()


tk.Label(root, text="Recipent's Email: ").pack()
recipent_entry = tk.Entry(root, width=50)
recipent_entry.pack()


tk.Label(root, text="Subject: ").pack()
subject_entry = tk.Entry(root, width=50)
subject_entry.pack()


tk.Label(root, text="Message: ").pack()
message_entry = tk.Text(root, height=10, width=50)
message_entry.pack()



send_btn = tk.Button(root, text="Send Email", command=send_email)
send_btn.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()


root.mainloop()

