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

def print_header():
    """Prints a stylish header for the application."""
    console.print(Panel(
        Text("Paystack Transaction Verifier", justify="center", style="bold blue"),
        title="[bold green]Welcome[/bold green]",
        border_style="cyan"
    ))
    console.print()
    
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

def display_results(data):
    """
    Displays the transaction details in a formatted table.

    Args:
        data (dict): The dictionary containing transaction details.
    """
    if not data:
        console.print("\nCould not retrieve transaction details.", style="bold red")
        return

    table = Table(title="Paystack Transaction Details", style="cyan", title_style="bold magenta")
    table.add_column("Field", style="green", no_wrap=True)
    table.add_column("Value", style="white")

    status = data.get('status', 'N/A')
    # Paystack amount is in kobo (the smallest currency unit), so divide by 100
    amount = data.get('amount', 0) / 100
    currency = data.get('currency', '')
    
    table.add_row("Status", status.title())
    table.add_row("Reference", data.get('reference', 'N/A'))
    table.add_row("Amount", f"{amount:,.2f} {currency}")
    table.add_row("Customer Email", data.get('customer', {}).get('email', 'N/A'))
    table.add_row("Transaction Date", data.get('paid_at', data.get('created_at', 'N/A')))
    table.add_row("Channel", data.get('channel', 'N/A'))
    
    # Style the status row based on the result for clear visual feedback
    if status == 'success':
        table.rows[0].style = "bold green"
    else:
        table.rows[0].style = "bold red"

    console.print()
    console.print(table)

def main():
    """Main function to run the verifier tool."""
    print_header()
    
    while True:
        # Use getpass to securely ask for the secret key without showing it on screen
        try:
            api_key = getpass.getpass(prompt="Enter your Paystack Secret Key: ")
        except Exception as error:
            console.print(f"Could not read API key: {error}", style="bold red")
            continue

        reference = input("Enter the transaction reference: ")

        if not api_key or not reference:
            console.print("API Key and Reference cannot be empty.", style="bold red")
            continue

        result_data = verify_paystack(api_key, reference)
        display_results(result_data)

        console.print("\n----------------------------------------\n", style="dim")
        again = input("Do you want to verify another transaction? (y/n): ").lower()
        if again != 'y':
            console.print("Goodbye!", style="bold blue")
            break
        console.print()


if __name__ == "__main__":
    main()

