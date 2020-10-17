from dateutil.relativedelta import relativedelta
from django.test import TestCase
from datetime import date, timedelta

from .utils import compute_age

#time_now = date.now()
#ten_years = time_now - relativedelta(years=10)
#five_days_less = ten_years - timedelta(days=5)
#twenty_days_less = ten_years - timedelta(days=20)
#ten_days_more = ten_years + timedelta(days=10)
#twenty_five_days_more = ten_years + timedelta(days=15)
#
#@pytest.mark.parametrize("")
#def test_compute_age():
#    pass


def test_ten_years():
    time_now = date.today()
    ten_years = time_now - relativedelta(years=10)
    age = compute_age(ten_years)
    assert age['years'] == 10

def test_before_bd_less_five():
    time_now = date.today()
    bd = time_now - relativedelta(years=10) - timedelta(days=5)
    age = compute_age(bd)
    assert age['years'] == 10
    assert age['months'] == 0

def test_before_bd_less_twenty():
    time_now = date.today()
    bd = time_now - relativedelta(years=10) - timedelta(days=20)
    age = compute_age(bd)
    assert age['years'] == 10
    assert age['months'] == 1

def test_after_bd_plus_five():
    time_now = date.today()
    bd = time_now -relativedelta(years=10) + timedelta(days=5)
    age = compute_age(bd)
    assert age['years'] == 10
    assert age['months'] == 0

def test_after_bd_plus_twenty():
    time_now = date.today()
    bd = time_now - relativedelta(years=10) + timedelta(days=20)
    age = compute_age(bd)
    assert age['years'] == 9
    assert age['months'] == 11
