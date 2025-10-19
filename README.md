# Paystack Transaction Verifier CLI

A clean, fast, and user-friendly command-line tool to instantly verify the status and details of any Paystack transaction directly from your terminal.

This CLI tool provides a near-instant way to check a transaction's status without ever leaving your terminal, saving you time and keeping you in your workflow.

## Features

- **Direct Verification:** Instantly fetch transaction details using a reference string.  
- **Secure Input:** Your Paystack Secret Key is entered securely and is never displayed on screen or stored.  
- **Readable Output:** Transaction details are displayed in a clean, color-coded table for easy reading.  
- **Robust Error Handling:** Gracefully handles invalid input, API errors, and network issues.  
- **User-Friendly:** Includes a retry limit for invalid input and an explicit quit command, so you're always in control.

## Requirements

- Python 3.7+

## Installation & Setup

Follow these steps to get the tool up and running in under two minutes.

### 1. Clone the Repository

```bash
git clone https://github.com/jola-ds/fintech-transaction-verifier.git
cd fintech-transaction-verifier
```

### 2. (Recommended) Create a Virtual Environment

```bash
python -m venv venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Your Paystack Credentials

To use this tool, you will need a **Test Secret Key** and a **Transaction Reference** from your Paystack developer account.

1. Sign up for a free account on the [Paystack Dashboard](https://dashboard.paystack.com/).  
2. Make sure you are in **Test Mode**.  
3. Go to **Settings → API Keys & Webhooks** to find your **Test Secret Key**.  
4. Go to **Transactions** to find a **Reference** from a test payment.  
   *(You may need to create one first using a Payment Page.)*

### 5. Usage

```bash
# Run the script from your terminal
python transaction_verifier.py
```

## Technology

- Python 3
- Requests
- Rich

## License

This project is licensed under the MIT License.
