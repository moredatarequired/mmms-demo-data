import math
import random
from datetime import datetime, time, timedelta


def random_gamma_ceil(avg):
    return math.ceil(random.gammavariate(avg, 1))


def to_datetime(d):
    return datetime.combine(d, time())


def random_date_range(fake, start=None, end=None):
    if start is None:
        start = datetime(year=1972, month=1, day=1)  # Arbitrary start date.
    if end is None:
        end = datetime.today() + timedelta(days=365)

    start_date = to_datetime(fake.date_between(start_date=start, end_date=end))

    duration = random_gamma_ceil(365)
    end_date = start_date + timedelta(duration)
    if end_date > end:
        end_date = end
    if end_date > datetime.today() + timedelta(days=365):
        end_date = None

    return start_date, end_date


def random_seed():
    return random.getrandbits(64)
