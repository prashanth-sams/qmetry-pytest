import pytest
from unittest.mock import patch, mock_open, MagicMock
from qmetry_pytest.plugin import QMetryApi, QMetryPytestPlugin


def test_qmetry_api_init_with_properties_file():
    with patch(
        "builtins.open",
        mock_open(
            read_data="qmetry.enabled=true\nqmetry.url=http://example.com\nqmetry.authorization=auth_token\nqmetry.automation.enabled=true\nqmetry.automation.apikey=api_key\nqmetry.automation.resultfile=result.xml"
        ),
    ):
        with patch("os.path.exists", return_value=True):
            qmetry_api = QMetryApi()
            assert qmetry_api.properties["qmetry.enabled"] == "true"
            assert qmetry_api.properties["qmetry.url"] == "http://example.com"
            assert qmetry_api.properties["qmetry.authorization"] == "auth_token"
            assert qmetry_api.properties["qmetry.automation.enabled"] == "true"
            assert qmetry_api.properties["qmetry.automation.apikey"] == "api_key"
            assert qmetry_api.properties["qmetry.automation.resultfile"] == "result.xml"


def test_qmetry_api_init_without_properties_file():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            QMetryApi()


def test_validate_qmetry_config():
    with patch(
        "builtins.open",
        mock_open(
            read_data="qmetry.enabled=true\nqmetry.automation.enabled=true\nqmetry.url=http://example.com\nqmetry.authorization=auth_token\nqmetry.automation.apikey=api_key\nqmetry.automation.resultfile=result.xml"
        ),
    ):
        with patch("os.path.exists", return_value=True):
            qmetry_api = QMetryApi()
            is_valid, flow_type, error_message = qmetry_api.validate_qmetry_config()
            assert is_valid
            assert flow_type == "automation"
            assert error_message is None


def test_validate_qmetry_config_invalid():
    with patch(
        "builtins.open",
        mock_open(
            read_data="qmetry.enabled=true\nopenapi.qmetry.enabled=true\nqmetry.automation.enabled=true"
        ),
    ):
        with patch("os.path.exists", return_value=True):
            qmetry_api = QMetryApi()
            is_valid, flow_type, error_message = qmetry_api.validate_qmetry_config()
            assert not is_valid
            assert flow_type is None
            assert (
                error_message
                == "openapi.qmetry.enabled and qmetry.automation.enabled cannot be both true or both false"
            )


def test_pytest_addoption():
    parser = MagicMock()
    QMetryPytestPlugin.pytest_addoption(parser)
    parser.getgroup.assert_called_with("qmetry")
    parser.getgroup().addoption.assert_called_with(
        "--qmetry",
        action="store_true",
        default=False,
        help="Enable QMetry test results reporting",
    )


def test_pytest_configure():
    config = MagicMock()
    config.getoption.return_value = True
    with patch("qmetry_pytest.plugin.QMetryApi") as MockQMetryApi:
        mock_qmetry_api = MockQMetryApi.return_value
        mock_qmetry_api.properties = {"qmetry.enabled": "true"}
        mock_qmetry_api.validate_qmetry_config.return_value = (True, "automation", None)
        QMetryPytestPlugin.pytest_configure(config)
        assert QMetryPytestPlugin.q is True


@pytest.mark.skip
def test_pytest_runtest_makereport():
    item = MagicMock()
    item.keywords = {"qid": "TC-123"}
    call = MagicMock()
    outcome = MagicMock()
    outcome.get_result.return_value = call
    call.when = "call"
    call.failed = True
    plugin = QMetryPytestPlugin()
    plugin.pytest_runtest_makereport(item, call)
    outcome.get_result.assert_called_once()


@pytest.mark.skip
def test_pytest_sessionfinish():
    session = MagicMock()
    with patch("qmetry_pytest.plugin.QMetryApi") as MockQMetryApi:
        mock_qmetry_api = MockQMetryApi.return_value
        mock_qmetry_api.properties = {"qmetry.enabled": "true"}
        plugin = QMetryPytestPlugin()
        plugin.q = True
        plugin.create_test_execution = MagicMock()
        plugin.pytest_sessionfinish(session)
        plugin.create_test_execution.assert_called_once()


@pytest.mark.skip
def test_create_test_execution():
    plugin = QMetryPytestPlugin()
    plugin.q = True
    plugin.flow_type = "automation"
    plugin._automation_import_result = MagicMock(
        return_value="http://example.com/upload"
    )
    plugin._automation_upload_file = MagicMock()
    plugin.create_test_execution()
    plugin._automation_import_result.assert_called_once()
    plugin._automation_upload_file.assert_called_once_with("http://example.com/upload")
