from datetime import datetime, timedelta


def now_str(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime.now().strftime(fmt)


def today_str(fmt: str = "%Y-%m-%d") -> str:
    return datetime.now().strftime(fmt)


def days_from_now(days: int, fmt: str = "%Y-%m-%d") -> str:
    return (datetime.now() + timedelta(days=days)).strftime(fmt)


def parse_date(value: str, fmt: str = "%Y-%m-%d") -> datetime:
    return datetime.strptime(value, fmt)
