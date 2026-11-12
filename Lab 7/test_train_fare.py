
from hypothesis import given, strategies as st
from train_fare import parse_pnr, journey_distance, berth_type


# Test 1: PNR parsing should not crash
@given(st.text() | st.none())
def test_parse_pnr_no_crash(s):
    parse_pnr(s)


# Test 2: Journey distance should not crash
@given(st.text() | st.none())
def test_journey_distance_no_crash(s):
    journey_distance(s)


# Test 3: Berth type identification should not crash
@given(st.text() | st.none())
def test_berth_type_no_crash(s):
    berth_type(s)
