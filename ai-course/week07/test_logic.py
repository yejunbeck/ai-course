import unittest
import os
import json
from logic import AccountBookLogic

class TestAccountBookLogic(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_data.json"
        self.logic = AccountBookLogic(file_path=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_entry_success(self):
        success, msg = self.logic.add_entry("수입", 10000, "식비", "월급")
        self.assertTrue(success)
        self.assertEqual(len(self.logic.get_all_entries()), 1)
        self.assertEqual(self.logic.get_all_entries()[0]['amount'], 10000)

    def test_add_entry_invalid_amount(self):
        success, msg = self.logic.add_entry("지출", -500, "식비", "잘못된 금액")
        self.assertFalse(success)
        self.assertEqual(msg, "금액은 0보다 큰 정수여야 합니다.")

    def test_summary_calculation(self):
        self.logic.add_entry("수입", 5000, "기타", "수입1")
        self.logic.add_entry("지출", 2000, "식비", "지출1")
        self.logic.add_entry("지출", 1000, "교통", "지출2")
        
        summary = self.logic.get_summary()
        self.assertEqual(summary['total_income'], 5000)
        self.assertEqual(summary['total_expense'], 3000)
        self.assertEqual(summary['balance'], 2000)

    def test_delete_entry(self):
        self.logic.add_entry("수입", 1000, "기타", "삭제대상")
        self.assertEqual(len(self.logic.get_all_entries()), 1)
        
        success = self.logic.delete_entry(0)
        self.assertTrue(success)
        self.assertEqual(len(self.logic.get_all_entries()), 0)

if __name__ == "__main__":
    unittest.main()
