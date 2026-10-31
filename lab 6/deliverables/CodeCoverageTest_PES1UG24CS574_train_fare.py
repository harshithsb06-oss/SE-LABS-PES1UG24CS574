
import pytest
from train_fare import base_fare, concession, tatkal_charge


# Base fare tests
def test_sleeper_fare():
    assert base_fare("SL", 500) == 500


def test_other_class_fares():
    assert base_fare("3A", 100) == 200
    assert base_fare("2A", 100) == 300
    assert base_fare("1A", 100) == 500


def test_minimum_fare():
    assert base_fare("SL", 10) == 50


def test_unknown_class():
    with pytest.raises(ValueError, match="unknown class"):
        base_fare("XX", 100)


def test_zero_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", 0)


def test_negative_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", -10)


# Concession tests
def test_adult_no_concession():
    assert concession(30, "M", False) == 0


def test_child_under_five():
    assert concession(4, "M", False) == 100


def test_child_concession():
    assert concession(8, "M", False) == 50


def test_senior_female():
    assert concession(60, "F", False) == 50


def test_senior_male():
    assert concession(60, "M", False) == 40


def test_tatkal_disables_concession():
    assert concession(8, "M", True) == 0


# Tatkal charge tests
def test_sleeper_tatkal():
    assert tatkal_charge("SL", 1000) == 100


def test_sleeper_charge_below_minimum():
    assert tatkal_charge("SL", 500) == 100


def test_other_class_tatkal():
    assert tatkal_charge("3A", 1000) == 300


def test_tatkal_charge_minimum():
    assert tatkal_charge("3A", 100) == 100


def test_tatkal_charge_maximum():
    assert tatkal_charge("3A", 2000) == 400
