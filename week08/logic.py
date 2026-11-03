from datetime import datetime
import math

def calculate_parking_fee(entry_dt: datetime, exit_dt: datetime):
    """
    입차 및 출차 시각을 바탕으로 주차 시간(분)과 요금을 계산합니다.
    
    Args:
        entry_dt (datetime): 입차 일시
        exit_dt (datetime): 출차 일시
        
    Returns:
        tuple: (주차 시간(분), 계산된 요금)
        
    Raises:
        ValueError: 출차 시각이 입차 시각보다 빠를 경우
    """
    if exit_dt <= entry_dt:
        raise ValueError("출차 시각은 입차 시각보다 이후여야 합니다.")

    # 총 주차 시간 계산 (분 단위)
    duration = exit_dt - entry_dt
    total_minutes = duration.total_seconds() / 60

    # 요금 계산 로직
    if total_minutes <= 30:
        fee = 0
    else:
        # 30분 이후의 시간 계산
        extra_minutes = total_minutes - 30
        # 10분 단위 올림 적용
        intervals = math.ceil(extra_minutes / 10)
        fee = intervals * 500

    # 최대 요금 제한 (20,000원)
    if fee > 20000:
        fee = 20000

    return int(total_minutes), int(fee)

def format_currency(amount: int) -> str:
    """
    금액을 천 단위 구분 기호가 포함된 한국어 금액 형식으로 변환합니다.
    예: 15500 -> 15,500원
    """
    return f"{amount:,}원"
