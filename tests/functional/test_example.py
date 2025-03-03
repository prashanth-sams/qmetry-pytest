import pytest


# For OpenAPI flow, tests need QMetry ID markers
@pytest.mark.qid("TC-122")
@pytest.mark.smoke
def test_example_2():
    assert True


# @pytest.mark.qid("TC-124")
def test_another_example_2():
    assert 1 + 1 == 3


# For Automation flow, no markers needed - all tests will be reported
def test_example_automation_2():
    assert True
