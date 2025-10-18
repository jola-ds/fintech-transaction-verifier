"""A command-line tool to verify Paystack transactions.

This script uses the Paystack API to fetch and display the status and
details of a given transaction reference. It prompts the user for their
secret key and the transaction reference securely.
"""
import getpass
import sys
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Initialize Rich console for terminal output
console = Console()

PAYSTACK_API_URL = "https://api.paystack.co/transaction/verify/"
MAX_INPUT_ATTEMPTS = 3

def print_header():
    """Prints a stylish header for the application."""
    console.print(Panel(
        Text("Paystack Transaction Verifier", justify="center", style="bold blue"),
        title="[bold green]Welcome[/bold green]",
        border_style="cyan"
    ))
    console.print()

def get_user_input():
    """
    Prompts the user for API key and reference, handling retries and quit commands.

    Returns:
        tuple: A tuple containing (api_key, reference) or (None, None) if the user quits
               or fails to provide input after MAX_INPUT_ATTEMPTS.
    """
    for attempt in range(MAX_INPUT_ATTEMPTS):
        try:
            console.print("\nType 'quit' or 'exit' at any time to leave.", style="dim yellow")
            # Prompt for API Key
            api_key_prompt = "Enter your Paystack Secret Key: "
            api_key = getpass.getpass(prompt=api_key_prompt)
            if api_key.lower() in ['quit', 'exit']:
                return (None, None)

            # Prompt for Reference
            reference_prompt = "Enter the transaction reference: "
            reference = input(reference_prompt)
            if reference.lower() in ['quit', 'exit']:
                return (None, None)

            # Check if input is valid
            if api_key and reference:
                return (api_key, reference)

                        # If input is invalid, print a warning
            remaining_attempts = MAX_INPUT_ATTEMPTS - (attempt + 1)
            error_message = (
                f"API Key and Reference cannot be empty. "
                f"You have {remaining_attempts} attempts left."
            )
            console.print(error_message, style="bold red")

        except (KeyboardInterrupt, EOFError):
            # Handle Ctrl+C or Ctrl+D gracefully
            return (None, None)

    # If the loop finishes, it means the user has run out of attempts
    console.print("\nToo many failed attempts. Exiting.", style="bold red")
    return (None, None)

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
        # Get input from the new, robust function
        api_key, reference = get_user_input()

        # If the function returns None, the user wants to quit or has failed.
        if not api_key:
            break

        result_data = verify_paystack(api_key, reference)
        display_results(result_data)

        console.print("\n----------------------------------------\n", style="dim")
        again = input("Do you want to verify another transaction? (y/n): ").lower()
        if again != 'y':
            break

    console.print("Goodbye!", style="bold blue")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Catch Ctrl+C on the "verify another" prompt
        console.print("\nGoodbye!", style="bold blue")
        sys.exit(0)
