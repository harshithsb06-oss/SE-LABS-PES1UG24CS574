
import pytest

from train_fare import base_fare, concession, tatkal_charge


# Base fare: class validation
def test_valid_class():
    assert base_fare("SL", 100) == 100


def test_unknown_class():
    with pytest.raises(ValueError, match="unknown class"):
        base_fare("XX", 100)


# Base fare: distance validation
def test_zero_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", 0)


def test_negative_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", -10)


# Base fare: minimum fare condition
def test_fare_below_minimum():
    assert base_fare("SL", 10) == 50


def test_fare_above_minimum():
    assert base_fare("SL", 100) == 100


# Concession: Tatkal condition
def test_tatkal_disables_concession():
    assert concession(8, "M", True) == 0


def test_non_tatkal_concession():
    assert concession(8, "M", False) == 50


# Concession: age conditions
def test_age_below_five():
    assert concession(4, "M", False) == 100


def test_age_five_to_twelve():
    assert concession(8, "M", False) == 50


def test_age_above_twelve_below_sixty():
    assert concession(30, "M", False) == 0


def test_age_sixty_or_above():
    assert concession(60, "M", False) == 40


# Concession: gender condition for senior citizens
def test_senior_female():
    assert concession(60, "F", False) == 50


def test_senior_male():
    assert concession(60, "M", False) == 40


# Tatkal: class condition
def test_sleeper_tatkal_charge():
    assert tatkal_charge("SL", 1000) == 100


def test_non_sleeper_tatkal_charge():
    assert tatkal_charge("3A", 1000) == 300


# Tatkal: maximum charge condition
def test_charge_above_maximum():
    assert tatkal_charge("3A", 2000) == 400


def test_charge_not_above_maximum():
    assert tatkal_charge("3A", 1000) == 300


# Tatkal: minimum charge condition
def test_charge_below_minimum():
    assert tatkal_charge("3A", 100) == 100


def test_charge_above_minimum():
    assert tatkal_charge("3A", 1000) == 300
