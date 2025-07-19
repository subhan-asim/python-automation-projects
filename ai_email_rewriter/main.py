import tkinter as tk
from tkinter import messagebox
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
#USE .env if you know how to, I used input for non nerdy people.
API_KEY = input("Enter your Api Key: ")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "https://example.com",  # Change this to your own domain/github
    "X-Title": "Email Rewriter App",
    "Content-Type": "application/json"
}

def rewrite_email():
    original = input_text.get("1.0", tk.END).strip()
    tone = tone_var.get()
    limit = max_words.get().strip()
    if limit:
        if limit.isdigit():
            limit = int(limit)
            pass
        else:
            status_label.config(text="Kindly enter an int in max words.")
            return

    if not original:
        status_label.config(text="Please enter your email text.")
        return
    if not limit:
        prompt=f"Rewrite the following email in a {tone} tone:\n\n{original}\n\nOnly return the rewritten email. Do not include any thoughts, notes, reasoning, or additional explanation. Output only the rewritten email itself. No introductions. No summaries. No formatting tags. No commentary."    
    else:
        prompt = f"Rewrite the following email in a {tone} tone, keeping it under {limit} words:\n\n{original}\n\nOnly return the rewritten email. Do not include any thoughts, notes, reasoning, or additional explanation. Output only the rewritten email itself. No introductions. No summaries. No formatting tags. No commentary."    

    payload = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Will raise exception for 400/401/500, etc.

        data = response.json()
        output = data["choices"][0]["message"]["content"].strip()

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, output)

    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"{response.status_code}: {response.text}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def copy_to_clipboard():
    text = output_text.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    status_label.config(text="Copied to clipboard!")
    root.after(2000, lambda: status_label.config(text=""))

def clear_fields():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    status_label.config(text="")
    max_words.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Email Rewriter")

tk.Label(root, text="Enter your email:").pack()
input_text = tk.Text(root, height=10, width=50)
input_text.pack()

tk.Label(root, text="Enter Max Words (leave blanks if no limit)").pack()
max_words = tk.Entry(root, width=5)
max_words.pack()

tk.Label(root, text="Select tone:").pack()
tone_var = tk.StringVar(value="friendly")
tk.OptionMenu(root, tone_var, "friendly", "professional", "casual", "strict").pack()

tk.Button(root, text="Rewrite Email", command=rewrite_email).pack()

tk.Label(root, text="Rewritten Email:").pack()
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

tk.Button(root, text="Copy to clipboard", command=copy_to_clipboard).pack()

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

tk.Button(root, text="Clear", command=clear_fields).pack()


root.mainloop()