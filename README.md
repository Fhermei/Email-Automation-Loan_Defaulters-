# Loan Reminder System

A simple application to send payment reminders to loan defaulters.

## Features ✨
- Automated email reminders for overdue loans
- Retry mechanism for failed email deliveries (2 attempts)
- Secure credential management using `.env` file
- Continuous operation with 2-day intervals
- Simple CSV data integration
- Console logging and status updates

## Setup 🛠️

### Requirements
- Python 3.6+
- Required packages: `pandas`, `yagmail`, `python-dotenv`

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/loan-reminder-system.git

pip install -r requirements.txt
