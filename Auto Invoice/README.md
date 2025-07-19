
📦 INVOICE SENDER TOOL - USAGE GUIDE

🔧 REQUIREMENTS:
- Checkout requirements.txt.
- Do NOT delete .env, clients.xlsx.

📄 HOW TO USE:

1. Open clients.xlsx and enter client data starting from row 2.
   Make sure the columns are:
   Name | Email | Item | Qty | Price | Due Date

2. Save and close the Excel file.

3. Double-click invoice_sender.exe  
   The tool will:
   ✅ Create invoice text files  
   ✅ Generate PDFs  
   ✅ Automatically send them to each client's email

⚠ Make sure your .env file is properly filled before running.

.env file should look like this:
EMAIL=your_email@gmail.com  
APP_PASSWORD=your_app_password_from_google

✅ That’s it! You’ll see a success message for each invoice sent.