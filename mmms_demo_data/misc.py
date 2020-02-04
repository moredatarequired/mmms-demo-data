import math
import random
from datetime import date, timedelta


def random_gamma_ceil(avg):
    return math.ceil(random.gammavariate(avg, 1))


def random_date_range(fake, start=None, end=None):
    if start is None:
        start = date(year=1972, month=1, day=1)  # Arbitrary start date.
    if end is None:
        end = date.today() + timedelta(days=3650)

    start_date = fake.date_between(start_date=start, end_date=end)
    end_date = fake.date_between(start_date=start_date, end_date=end)

    if end_date > date.today() + timedelta(days=365):
        end_date = None

    return start_date, end_date
