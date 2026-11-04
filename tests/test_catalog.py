from pathlib import Path

import pytest

from bord4_analysis_templates import (
    TemplateExistsError,
    copy_template,
    get_template,
    list_templates,
    read_template,
    template_path,
)


def test_manifest_matches_template_files() -> None:
    manifest_names = {template.name for template in list_templates()}
    source_names = {path.name for path in Path("templates").glob("*.py")}

    assert manifest_names == source_names


def test_read_template() -> None:
    template = get_template("etl-read-csv.py")

    assert template.destination == "notebooks"
    assert "pakkenellik>=0.2.4" in template.dependencies
    assert "# # Extract, transform and load (ETL)" in read_template(template.name)


def test_copy_template_uses_manifest_defaults(tmp_path: Path) -> None:
    output_path = copy_template("etl-read-csv.py", project_dir=tmp_path)

    assert output_path == tmp_path / "notebooks" / "01-etl-read-csv.py"
    assert output_path.read_text(encoding="utf-8") == read_template("etl-read-csv.py")


def test_copy_template_does_not_overwrite(tmp_path: Path) -> None:
    copy_template("etl-read-csv.py", project_dir=tmp_path)

    with pytest.raises(TemplateExistsError):
        copy_template("etl-read-csv.py", project_dir=tmp_path)


def test_copy_template_accepts_name_without_suffix(tmp_path: Path) -> None:
    output_path = copy_template(
        "etl-read-csv.py",
        project_dir=tmp_path,
        output_name="fetch-data",
    )

    assert output_path.name == "fetch-data.py"


def test_template_path_resolves_suffix_without_writing(tmp_path: Path) -> None:
    output_path = template_path(
        "etl-read-csv.py",
        project_dir=tmp_path,
        output_name="fetch-data",
    )

    assert output_path == tmp_path / "notebooks" / "fetch-data.py"
    assert not output_path.exists()
