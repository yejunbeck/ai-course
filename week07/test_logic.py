import logic

def test_logic():
    passed = 0
    failed = 0

    # Test case 1: Initial load
    data = logic.load_data()
    assert isinstance(data, list), "Data should be a list"
    passed += 1

    # Test case 2: add_item valid
    test_data = []
    test_data, err = logic.add_item(test_data, "Salary", 1000, "수입")
    assert err == "", f"Expected no error, got {err}"
    assert len(test_data) == 1
    assert test_data[0]["description"] == "Salary"
    assert test_data[0]["amount"] == 1000
    assert test_data[0]["category"] == "수입"
    passed += 1

    # Test case 3: add_item invalid (zero amount)
    test_data, err = logic.add_item(test_data, "Invalid", 0, "지출")
    assert err == "금액은 0보다 큰 정수여야 합니다."
    assert len(test_data) == 1
    passed += 1

    # Test case 4: add_item invalid (negative amount)
    test_data, err = logic.add_item(test_data, "Invalid", -100, "지출")
    assert err == "금액은 0보다 큰 정수여야 합니다."
    assert len(test_data) == 1
    passed += 1

    # Test case 5: add_item invalid (string amount)
    test_data, err = logic.add_item(test_data, "Invalid", "abc", "지출")
    assert err == "금액은 숫자여야 합니다."
    assert len(test_data) == 1
    passed += 1

    # Test case 6: calculate_totals
    test_data = [
        {"description": "S1", "amount": 1000, "category": "수입"},
        {"description": "S2", "amount": 500, "category": "수입"},
        {"description": "E1", "amount": 300, "category": "지출"},
        {"description": "E2", "amount": 200, "category": "지출"},
    ]
    inc, exp, bal = logic.calculate_totals(test_data)
    assert inc == 1500
    assert exp == 500
    assert bal == 1000
    passed += 1

    # Test case 7: delete_item
    test_data = [{"description": "X", "amount": 100, "category": "수입"}]
    test_data = logic.delete_item(test_data, 0)
    assert len(test_data) == 0
    passed += 1

    # Test case 8: delete_item out of range
    test_data = [{"description": "X", "amount": 100, "category": "수입"}]
    test_data = logic.delete_item(test_data, 5)
    assert len(test_data) == 1
    passed += 1

    # Test case 9: format_currency
    assert logic.format_currency(1234567) == "1,234,567"
    assert logic.format_currency(0) == "0"
    passed += 1

    print(f"Test results: {passed} passed, {failed} failed")

if __name__ == "__main__":
    test_logic()
