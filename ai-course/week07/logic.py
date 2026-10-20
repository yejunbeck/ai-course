import json
import os

class AccountBookLogic:
    def __init__(self, file_path="data.json"):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_data(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            return True
        except IOError:
            return False

    def add_entry(self, entry_type, amount, category, description):
        """
        entry_type: '수입' or '지출'
        amount: int
        category: str
        description: str
        """
        if not isinstance(amount, int) or amount <= 0:
            return False, "금액은 0보다 큰 정수여야 합니다."
        
        new_entry = {
            "type": entry_type,
            "amount": amount,
            "category": category,
            "description": description
        }
        self.data.append(new_entry)
        self.save_data()
        return True, ""

    def delete_entry(self, index):
        if 0 <= index < len(self.data):
            del self.data[index]
            self.save_data()
            return True
        return False

    def get_summary(self):
        total_income = sum(item['amount'] for item in self.data if item['type'] == '수입')
        total_expense = sum(item['amount'] for item in self.data if item['type'] == '지출')
        balance = total_income - total_expense
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        }

    def get_all_entries(self):
        return self.data
