from unittest.mock import patch, mock_open, MagicMock
from qmetry_pytest.config import QMetryConfig


def test_automation_import_result_header():
    with patch("qmetry_pytest.plugin.QMetryApi") as MockQMetryApi:
        mock_qmetry_api = MockQMetryApi.return_value
        mock_qmetry_api.properties = {
            "qmetry.automation.apikey": "test_api_key",
            "qmetry.authorization": "test_auth",
        }
        config = QMetryConfig()
        headers = config.automation_import_result_header()
        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"
        assert headers["apiKey"] == "test_api_key"
        assert headers["Authorization"] == "test_auth"


def test_automation_import_result_payload():
    with patch("qmetry_pytest.plugin.QMetryApi"):
        config = QMetryConfig()
        payload = config.automation_import_result_payload()
        assert payload["format"] == "cucumber"
        assert payload["attachFile"] is True


def test_automation_file_upload_header():
    with patch("qmetry_pytest.plugin.QMetryApi") as MockQMetryApi:
        mock_qmetry_api = MockQMetryApi.return_value
        mock_qmetry_api.properties = {
            "qmetry.automation.apikey": "test_api_key",
            "qmetry.authorization": "test_auth",
        }
        config = QMetryConfig()
        headers = config.automation_file_upload_header()
        assert headers["apiKey"] == "test_api_key"
        assert headers["Authorization"] == "test_auth"


def test_junit_to_cucumber():
    with patch("qmetry_pytest.plugin.QMetryApi") as MockQMetryApi:
        mock_qmetry_api = MockQMetryApi.return_value
        mock_qmetry_api.properties = {"qmetry.automation.resultfile": "result.xml"}
        config = QMetryConfig()
        with patch("xml.etree.ElementTree.parse") as mock_parse:
            mock_tree = MagicMock()
            mock_parse.return_value = mock_tree
            mock_root = MagicMock()
            mock_tree.getroot.return_value = mock_root
            mock_root.findall.return_value = [
                MagicMock(
                    get=MagicMock(
                        side_effect=lambda x: (
                            "testcase1" if x == "name" else "TestFeature"
                        )
                    )
                ),
                MagicMock(
                    get=MagicMock(
                        side_effect=lambda x: (
                            "testcase2" if x == "name" else "TestFeature"
                        )
                    )
                ),
            ]
            with patch("builtins.open", mock_open()) as mock_file:
                config.junit_to_cucumber()
                mock_file.assert_called_once_with("result.json", "w")
                mock_file().write.assert_called()
