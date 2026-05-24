import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_ID = "1M7l2HGx6KlVlzFyb4YruHN_Qx1Q2sPwjl-28QK6DXGI"
SHEET_TAB = "Flagged Orders"

# Load the Superstore dataset
df = pd.read_excel("sample_-_superstore.xls", engine="xlrd")

# Identify orders where profit is negative
flagged = df[df["Profit"] < 0][
    ["Order ID", "Customer Name", "Product Name", "Sales", "Profit"]
].copy()

flagged = flagged.sort_values("Profit")

print(f"Total rows: {len(df)}")
print(f"Flagged (unprofitable) orders: {len(flagged)}")

# Authenticate with Google Sheets
creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(SPREADSHEET_ID)

# Get or create the "Flagged Orders" tab
try:
    worksheet = spreadsheet.worksheet(SHEET_TAB)
    worksheet.clear()
    print(f'Cleared existing "{SHEET_TAB}" tab')
except gspread.exceptions.WorksheetNotFound:
    worksheet = spreadsheet.add_worksheet(title=SHEET_TAB, rows=len(flagged) + 1, cols=5)
    print(f'Created new "{SHEET_TAB}" tab')

# Round floats for readability
flagged["Sales"] = flagged["Sales"].round(2)
flagged["Profit"] = flagged["Profit"].round(2)

# Write header + rows
rows = [flagged.columns.tolist()] + flagged.values.tolist()
worksheet.update(rows)

print(f"Written {len(flagged)} rows to Google Sheets.")

# Send SMS via Twilio
twilio_client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
message = twilio_client.messages.create(
    body=f"Alert: {len(flagged)} unprofitable orders detected in latest report run",
    from_=os.environ["TWILIO_FROM"],
    to=os.environ["TWILIO_TO"],
)
print(f"SMS sent (SID: {message.sid})")
