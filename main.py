import pandas as pd
import yagmail
from datetime import datetime
from dotenv import load_dotenv
import os
import time


CHECK_INTERVAL = 172800  # 2 days in seconds
MAX_EMAIL_RETRIES = 2
DATA_FILE = "./Dataset/Fherm_Loan.csv"

def load_loan_data():
    """Load and process loan data from CSV file"""
    try:
        df = pd.read_csv(DATA_FILE)
        df['Due Date'] = pd.to_datetime(df['Due Date']).dt.date # Convert 'Due Date' to datetime and extract date
        return df
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

def find_defaulters(df):
    """Identify customers with overdue payments"""
    today = datetime.now().date()
    return df[df['Due Date'] <= today]

def create_email(row):
    """Generate email content for a defaulter"""
    return f"""
    <h1>Loan Payment Reminder</h1>
    <p>Dear <strong>{row['Name']}</strong>,</p>
    <br>
    <p>We hope this email finds you well. This is a friendly reminder that your outstanding loan balance of 
    <strong>${row['Outstanding Amount']}</strong> for your <em>{row['Loan Type']}</em> is overdue.</p>
    <br>
    <p>Your due date was: <strong>{row['Due Date']}</strong>.</p>
    <p>Please make your payment at the earliest to avoid additional charges.</p>
    <p>Contact our support team if you need assistance. Your reference ID is: <strong>{row['User ID']}</strong>.</p>
    <p>Thank you,<br>Mvlzerz App</p>
    """

def send_reminders(defaulters):
    """Send emails to defaulters with retry logic"""
    try:
        yag = yagmail.SMTP(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PWD'))

        for _, row in defaulters.iterrows():
            for attempt in range(MAX_EMAIL_RETRIES):
                try:
                    yag.send(
                        to=row['Email'],
                        subject="Urgent: Loan Payment Overdue",
                        contents=create_email(row)
                    )
                    print(f"Sent to {row['Email']}")
                    break
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed for {row['Email']}: {str(e)}")
                    time.sleep(5)
    except Exception as e:
        print(f"Email setup failed: {str(e)}")


def main():
    """Main program loop"""
    load_dotenv()

    if not all([os.getenv('EMAIL_USER'), os.getenv('EMAIL_PWD')]):
        print("Missing email credentials in .env file")
        return

    while True:
        print("\nChecking for defaulters...")
        df = load_loan_data()

        if df is not None:
            defaulters = find_defaulters(df)
            if not defaulters.empty:
                print(f"Found {len(defaulters)} defaulters")
                send_reminders(defaulters)
            else:
                print("No defaulters found")

        print(f"Waiting {CHECK_INTERVAL // 86400} days...")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()