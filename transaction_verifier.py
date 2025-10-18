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