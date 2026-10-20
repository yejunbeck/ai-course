from dataclasses import dataclass
from datetime import datetime, timedelta
import math

@dataclass
class ParkingRecord:
    """주차 기록을 담는 데이터 클래스"""
    entry_datetime: datetime
    exit_datetime: datetime
    duration: timedelta
    fee: int

class ParkingCalculator:
    """요금 계산 로직을 담당하는 클래스"""
    
    FREE_DURATION_MINUTES = 30
    UNIT_DURATION_MINUTES = 10
    UNIT_FEE = 500
    MAX_FEE = 20000

    @staticmethod
    def calculate(entry_dt: datetime, exit_dt: datetime) -> ParkingRecord:
        if exit_dt <= entry_dt:
            raise ValueError("출차 시각은 입차 시각보다 이후여야 합니다.")

        duration = exit_dt - entry_dt
        duration_minutes = duration.total_seconds() / 60

        if duration_minutes <= ParkingCalculator.FREE_DURATION_MINUTES:
            fee = 0
        else:
            # 30분을 초과한 시간 계산
            extra_minutes = duration_minutes - ParkingCalculator.FREE_DURATION_MINUTES
            # 10분 단위로 올림 처리 (10분이 안 되는 나머지 시간도 10분으로 간주)
            units = math.ceil(extra_minutes / ParkingCalculator.UNIT_DURATION_MINUTES)
            fee = units * ParkingCalculator.UNIT_FEE

        # 최대 요금 제한 적용
        fee = min(fee, ParkingCalculator.MAX_FEE)

        return ParkingRecord(
            entry_datetime=entry_dt,
            exit_datetime=exit_dt,
            duration=duration,
            fee=fee
        )

class ParkingManager:
    """주차 기록 목록을 관리하는 클래스"""
    
    def __init__(self):
        self.records: list[ParkingRecord] = []

    def add_record(self, record: ParkingRecord):
        self.records.append(record)

    def remove_record(self, index: int):
        if 0 <= index < len(self.records):
            self.records.pop(index)
        else:
            raise IndexError("삭제할 기록이 존재하지 않습니다.")

    def get_total_fee(self) -> int:
        return sum(record.fee for record in self.records)

    def get_all_records(self) -> list[ParkingRecord]:
        return self.records
