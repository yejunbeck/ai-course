import unittest
from datetime import datetime, timedelta
from logic import ParkingCalculator, ParkingManager

class TestParkingLogic(unittest.TestCase):

    def test_calculate_free_period(self):
        """30분 이내 주차는 0원이어야 함"""
        entry = datetime(2023, 10, 20, 10, 0)
        exit_dt = datetime(2023, 10, 20, 10, 29)
        record = ParkingCalculator.calculate(entry, exit_dt)
        self.assertEqual(record.fee, 0)

    def test_calculate_exact_30min(self):
        """정확히 30분 주차는 0원이어야 함"""
        entry = datetime(2023, 10, 20, 10, 0)
        exit_dt = datetime(2023, 10, 20, 10, 30)
        record = ParkingCalculator.calculate(entry, exit_dt)
        self.assertEqual(record.fee, 0)

    def test_calculate_standard_fee(self):
        """40분 주차 시 500원이어야 함 (30분 무료 + 10분 500원)"""
        entry = datetime(2023, 10, 20, 10, 0)
        exit_dt = datetime(2023, 10, 20, 10, 40)
        record = ParkingCalculator.calculate(entry, exit_dt)
        self.assertEqual(record.fee, 500)

    def test_calculate_rounding_up(self):
        """31분 주차 시 500원, 41분 주차 시 1000원이어야 함 (올림 적용)"""
        entry = datetime(2023, 10, 20, 10, 0)
        
        # 31분
        record1 = ParkingCalculator.calculate(entry, datetime(2023, 10, 20, 10, 31))
        self.assertEqual(record1.fee, 500)
        
        # 41분
        record2 = ParkingCalculator.calculate(entry, datetime(2023, 10, 20, 10, 41))
        self.assertEqual(record2.fee, 1000)

    def test_max_fee_limit(self):
        """매우 긴 주차 시 최대 요금 20,000원이 적용되어야 함"""
        entry = datetime(2023, 10, 20, 10, 0)
        exit_dt = datetime(2023, 10, 21, 10, 0) # 24시간 주차
        record = ParkingCalculator.calculate(entry, exit_dt)
        self.assertEqual(record.fee, 20000)

    def test_overnight_parking(self):
        """날짜가 넘어가는 경우도 정확히 계산해야 함"""
        entry = datetime(2023, 10, 20, 23, 0)
        exit_dt = datetime(2023, 10, 21, 1, 0) # 2시간 주차
        record = ParkingCalculator.calculate(entry, exit_dt)
        # 120분 - 30분 = 90분. 90/10 = 9단위. 9 * 500 = 4500원
        self.assertEqual(record.fee, 4500)

    def test_invalid_time_order(self):
        """출차 시각이 입차보다 빠르면 ValueError가 발생해야 함"""
        entry = datetime(2023, 10, 20, 10, 0)
        exit_dt = datetime(2023, 10, 20, 9, 0)
        with self.assertRaises(ValueError):
            ParkingCalculator.calculate(entry, exit_dt)

    def test_manager_operations(self):
        """매니저의 추가, 삭제, 합계 기능 테스트"""
        manager = ParkingManager()
        
        # 데이터 1 생성 (500원)
        r1 = ParkingCalculator.calculate(datetime(2023, 10, 20, 10, 0), datetime(2023, 10, 20, 10, 40))
        # 데이터 2 생성 (1000원)
        r2 = ParkingCalculator.calculate(datetime(2023, 10, 20, 11, 0), datetime(2023, 10, 20, 11, 41))
        
        manager.add_record(r1)
        manager.add_record(r2)
        
        self.assertEqual(manager.get_total_fee(), 1500)
        self.assertEqual(len(manager.get_all_records()), 2)
        
        # 첫 번째 기록 삭제
        manager.remove_record(0)
        self.assertEqual(manager.get_total_fee(), 1000)
        self.assertEqual(len(manager.get_all_records()), 1)
        
        # 잘못된 인덱스 삭제 시도
        with self.assertRaises(IndexError):
            manager.remove_record(5)

if __name__ == "__main__":
    # unittest 기본 실행 방식 대신 요구사항대로 성공/실패 수 출력 커스텀
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParkingLogic)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    
    print("\n" + "="*30)
    print(f"테스트 완료!")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"실패: {len(result.failures)}")
    print(f"에러: {len(result.errors)}")
    print("="*30)
    
    if not result.wasSuccessful():
        exit(1)
