import json
import os

DATA_FILE = "data.json"

def load_data():
    """Load data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data):
    """Save data to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError:
        pass

def add_item(data, description, amount, category):
    """
    Add a new item to the list.
    Returns (updated_data, error_message)
    """
    try:
        amount_int = int(amount)
    except (ValueError, TypeError):
        return data, "금액은 숫자여야 합니다."

    if amount_int <= 0:
        return data, "금액은 0보다 큰 정수여야 합니다."
    
    new_item = {
        "description": str(description),
        "amount": amount_int,
        "category": category  # "수입" or "지출"
    }
    data.append(new_item)
    return data, ""

def delete_item(data, index):
    """Delete an item at the specified index."""
    if 0 <= index < len(data):
        data.pop(index)
    return data

def calculate_totals(data):
    """Calculate total income, expense, and balance."""
    total_income = sum(item["amount"] for item in data if item["category"] == "수입")
    total_expense = sum(item["amount"] for item in data if item["category"] == "지출")
    balance = total_income - total_expense
    return total_income, total_expense, balance

def format_currency(amount):
    """Format integer to thousand-separated string."""
    return f"{amount:,}"
