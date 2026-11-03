import unittest
from datetime import datetime, timedelta
from logic import calculate_parking_fee, format_currency

class TestParkingLogic(unittest.TestCase):

    def test_free_period(self):
        """30분 이내 주차 시 요금이 0원인지 확인"""
        entry = datetime(2023, 10, 20, 10, 0)
        exit = datetime(2023, 10, 20, 10, 30)
        minutes, fee = calculate_parking_fee(entry, exit)
        self.assertEqual(fee, 0)
        self.assertEqual(minutes, 30)

    def test_exact_ten_minute_intervals(self):
        """10분 단위 딱 맞게 계산되는지 확인 (예: 40분 주차 -> 30분 무료 + 10분 유료 = 500원)"""
        entry = datetime(2023, 10, 20, 10, 0)
        exit = datetime(2023, 10, 20, 10, 40)
        minutes, fee = calculate_parking_fee(entry, exit)
        self.assertEqual(fee, 500)

    def test_rounding_up(self):
        """10분이 안 되는 나머지 시간도 올림 처리되는지 확인 (예: 31분 주차 -> 500원)"""
        entry = datetime(2023, 10, 20, 10, 0)
        exit = datetime(2023, 10, 20, 10, 31)
        minutes, fee = calculate_parking_fee(entry, exit)
        self.assertEqual(fee, 500)

    def test_max_fee_limit(self):
        """최대 요금 20,000원이 적용되는지 확인"""
        # 10시간 주차 (600분)
        # 30분 무료 제외 -> 570분
        # 570 / 10 = 57 구간
        # 57 * 500 = 28,500원 -> 20,000원으로 제한되어야 함
        entry = datetime(2023, 10, 20, 10, 0)
        exit = datetime(2023, 10, 20, 20, 0) 
        minutes, fee = calculate_parking_fee(entry, exit)
        self.assertEqual(fee, 20000)

    def test_invalid_time(self):
        """출차 시각이 입차 시각보다 빠른 경우 ValueError 발생 확인"""
        entry = datetime(2023, 10, 20, 10, 0)
        exit = datetime(2023, 10, 20, 9, 0)
        with self.assertRaises(ValueError):
            calculate_parking_fee(entry, exit)

    def test_format_currency(self):
        """금액 포맷팅 확인"""
        self.assertEqual(format_currency(15500), "15,500원")
        self.assertEqual(format_currency(0), "0원")
        self.assertEqual(format_currency(1000000), "1,000,000원")

if __name__ == "__main__":
    # SPEC 요구사항: 실행 시 통과와 실패 수를 출력함
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParkingLogic)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    
    print("\n" + "="*30)
    print(f"결과 요약:")
    print(f"통과(Pass): {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"실패(Fail): {len(result.failures)}")
    print(f"에러(Error): {len(result.errors)}")
    print("="*30)
