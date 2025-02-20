# QMetry PyTest

A PyTest plugin that provides seamless integration with QMetry Test Management Platform.

## Features

- Automatically upload test execution results to QMetry
- Support for test case mapping and traceability
- Detailed test execution reporting
- Easy configuration through pytest.ini or command line arguments

## Installation

```
pip install qmetry-pytest
```

## Basic Setup

```
# conftest.py
from qmetry_pytest import QmetryPlugin

def pytest_configure(config):
    config.pluginmanager.register(QmetryPlugin())
```

## Configuration

You'll need to create a qmetry.properties file in your project root:
```
automation.qmetry.enabled=true
automation.qmetry.url=<your_qmetry_url>
automation.qmetry.apikey=<your_api_key>
automation.qmetry.testrunname=<test_run_name>
automation.qmetry.labels=<labels>
automation.qmetry.components=<components>
automation.qmetry.version=<version>
automation.qmetry.sprint=<sprint>
automation.qmetry.platform=<platform>
automation.qmetry.comment=<comment>
```

## Test Example

```
# test_example.py
import pytest

@pytest.mark.qid("TC-123")  # QMetry Test Case ID
def test_example():
    assert True

@pytest.mark.qid("TC-124")
def test_another_example():
    assert 1 + 1 == 2
```

## Test Execution

```
pytest --qmetry
```

## Key Features:

- Automatically uploads test results to QMetry
- Maps test cases with QMetry IDs
- Supports test case status updates
- Provides detailed test execution reports
- Can include attachments and screenshots

## Best Practices:

- Always include unique QMetry IDs for each test case
- Use meaningful test run names
- Keep configuration updated
- Handle authentication securely
- Include relevant metadata (components, versions, etc.)