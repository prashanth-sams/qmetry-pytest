import pytest


# For OpenAPI flow, tests need QMetry ID markers
@pytest.mark.qid("TC-123")
def test_example():
    assert True


# @pytest.mark.qid("TC-124")
def test_another_example():
    assert 1 + 1 == 3


# For Automation flow, no markers needed - all tests will be reported
def test_example_automation():
    assert True
