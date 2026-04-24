import pytest
from typer.testing import CliRunner
from unittest.mock import MagicMock, patch
from src.cli import app
from tests.data.cli_cases import (
    SINGLE_ROW_DB,
    MULTIPLE_ROW_DB,
    SEARCH_FILTERS,
    UPDATE_CASES,
)
from src.exceptions import (
    MissingSearchCriteria,
    EmptyField,
    EntryNotFound,
    MissingUpdateFields,
)

runner = CliRunner()


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_session(mock_db):
    with patch("src.cli.database_session") as patched:
        patched.return_value.__enter__.return_value = mock_db
        yield mock_db


# ---------------------CREATE---------------------#
@pytest.mark.cli_add
def test_add_valid_entry(mock_session):
    result = runner.invoke(app, ["add", "Microsoft", "DevOps"])

    assert result.exit_code == 0
    mock_session.add.assert_called_with({"company": "Microsoft", "job_title": "DevOps"})
    assert "Entry created successfully." in result.output


@pytest.mark.cli_add
@pytest.mark.parametrize("missing_field", ["company", "job_title"])
def test_add_missing_field(missing_field, mock_session):
    mock_session.add.side_effect = EmptyField(missing_field)
    result = runner.invoke(app, ["add", "Microsoft", "DevOps"])

    assert result.exit_code != 0
    assert f"Data for {missing_field} is missing." in result.output


# ---------------------READ---------------------#
# test command [list] from empty db
@pytest.mark.cli_list
def test_list_empty_db(mock_session):
    mock_session.get_all.return_value = []

    result = runner.invoke(app, "list")

    assert result.exit_code == 0
    assert "No entries found." in result.output


# test command [list] from single row db
@pytest.mark.cli_list
@pytest.mark.parametrize("case", SINGLE_ROW_DB)
def test_list_single_row_db(case, mock_session):
    mock_session.get_all.return_value = case

    result = runner.invoke(app, "list")

    assert result.exit_code == 0
    assert str(case[0]["id"]) in result.output
    assert case[0]["company"] in result.output
    assert case[0]["job_title"] in result.output
    assert case[0]["status"] in result.output


# test command [list] from multiple row db
@pytest.mark.cli_list
@pytest.mark.parametrize("case", MULTIPLE_ROW_DB)
def test_list_multiple_row_db(case, mock_session):
    mock_session.get_all.return_value = case

    result = runner.invoke(app, "list")

    assert result.exit_code == 0

    for entry in case:
        assert str(entry["id"]) in result.output
        assert entry["company"] in result.output
        assert entry["job_title"] in result.output
        assert entry["status"] in result.output


@pytest.mark.cli_search_by
@pytest.mark.parametrize("case", SEARCH_FILTERS)
def test_search_by_valid_filter(case, mock_session):
    result = runner.invoke(app, ["search-by"] + case["args"])

    assert result.exit_code == 0
    mock_session.get_by.assert_called_with(case["filter"])


@pytest.mark.cli_search_by
def test_search_by_empty_filter(mock_session):
    mock_session.get_by.side_effect = MissingSearchCriteria()
    result = runner.invoke(app, ["search-by"])

    assert result.exit_code != 0
    assert "No search criteria provided." in result.output


# --------------------UPDATE--------------------#
@pytest.mark.cli_update
@pytest.mark.parametrize("case", UPDATE_CASES)
def test_update_valid_entry(case, mock_session):
    result = runner.invoke(app, ["update", "1"] + case["args"])

    assert result.exit_code == 0
    mock_session.update.assert_called_with(1, case["data"])


@pytest.mark.cli_update
def test_update_invalid_id(mock_session):
    mock_session.update.side_effect = EntryNotFound(1)
    result = runner.invoke(app, ["update", "1", "--company", "Github"])

    assert result.exit_code != 0
    assert "Entry with id 1 not found." in result.output


@pytest.mark.cli_update
def test_update_empty_data(mock_session):
    mock_session.update.side_effect = MissingUpdateFields()
    result = runner.invoke(app, ["update", "1"])

    assert result.exit_code != 0
    assert "No fields provided for update." in result.output


# --------------------DELETE--------------------#
@pytest.mark.cli_delete
def test_delete_valid_entry(mock_session):
    result = runner.invoke(app, ["delete", "1"])

    assert result.exit_code == 0
    mock_session.delete.assert_called_with(1)
    assert "Job entry deleted successfully." in result.output


@pytest.mark.cli_delete
def test_delete_invalid_id(mock_session):
    mock_session.delete.side_effect = EntryNotFound(1)
    result = runner.invoke(app, ["delete", "1"])

    assert result.exit_code != 0
    assert "Entry with id 1 not found." in result.output


@pytest.mark.cli_delete
def test_reset_db_yes(mock_session):
    result = runner.invoke(app, ["reset"], input="y")

    assert result.exit_code == 0
    mock_session.delete_all.assert_called_once()
    assert "All entries were deleted successfully." in result.output


@pytest.mark.cli_delete
def test_reset_db_no(mock_session):
    result = runner.invoke(app, ["reset"], input="n")

    assert result.exit_code == 0
    mock_session.delete_all.assert_not_called()
    assert "Database reset aborted." in result.output


@pytest.mark.cli_delete
@pytest.mark.parametrize("case", ["m", "\n"])
def test_reset_db_wrong_input(case, mock_session):
    result = runner.invoke(app, ["reset"], input=case)

    assert result.exit_code != 0
    mock_session.delete_all.assert_not_called()
    assert "Invalid input provided." in result.output
