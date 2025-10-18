"""A command-line tool to verify Paystack transactions.

This script uses the Paystack API to fetch and display the status and
details of a given transaction reference. It prompts the user for their
secret key and the transaction reference securely.
"""
import getpass
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Initialize Rich console for terminal output
console = Console()

PAYSTACK_API_URL = "https://api.paystack.co/transaction/verify/"


def verify_paystack(api_key, reference):
    """
    Verifies a transaction using the Paystack API.

    Args:
        api_key (str): The user's Paystack secret key.
        reference (str): The transaction reference.

    Returns:
        dict: The transaction data if successful, None otherwise.
    """
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    url = f"{PAYSTACK_API_URL}{reference}"
    
    try:
        with console.status("[bold green]Verifying with Paystack...[/]"):
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        if data.get('status'):
            return data.get('data')
        else:
            console.print(f"Error: {data.get('message')}", style="bold red")
            return None

    except requests.exceptions.RequestException as e:
        console.print(f"An error occurred: {e}", style="bold red")
        return None
