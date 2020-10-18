import pytest
from dateutil.relativedelta import relativedelta
#from django.test import TestCase
from datetime import date, timedelta

from teams.utils import compute_age

time_now = date.today()
ten_years = time_now - relativedelta(years=10)
five_days_less = ten_years - timedelta(days=5)
twenty_days_less = ten_years - timedelta(days=20)
ten_days_more = ten_years + timedelta(days=10)
twenty_five_days_more = ten_years + timedelta(days=25)

testdata = [
    (ten_years, {'years': 10, 'months': 0}),
    (five_days_less, {'years': 10, 'months': 0}),
    (twenty_days_less, {'years': 10, 'months': 1}),
    (ten_days_more, {'years': 10, 'months': 0}),
    (twenty_five_days_more, {'years': 9, 'months': 11}),
]


@pytest.mark.parametrize("date, expected", testdata)
def test_compute_age(date, expected):
    age = compute_age(date)
    assert age == expected

