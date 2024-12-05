from datetime import timedelta
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent

DEFAULT_DESC = False
DEFAULT_LIMIT = 100
DEFAULT_OFFSET = 0
DEFAULT_ORDER_BY = "id"

ONE_MINUTE_SECONDS = int(timedelta(minutes=1).total_seconds())
ONE_DAY_SECONDS = int(timedelta(days=1).total_seconds())

ACCESS_TOKEN_EXPIRE_TIME_S = ONE_DAY_SECONDS * 3
REFRESH_TOKEN_EXPIRE_TIME_S = ONE_DAY_SECONDS * 7
TEMPORARY_TOKEN_EXPIRE_TIME_S = ONE_MINUTE_SECONDS * 5
