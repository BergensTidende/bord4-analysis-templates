from pathlib import Path
from typing import Protocol, cast

from bord4_analysis_templates.cli import main


class CaptureResult(Protocol):
    out: str
    err: str


class CaptureFixture(Protocol):
    def readouterr(self) -> CaptureResult: ...


def test_list_templates(capsys: object) -> None:
    assert main(["--list"]) == 0

    output = cast(CaptureFixture, capsys).readouterr()
    assert "etl-read-csv.py -> notebooks/01-etl-read-csv.py" in output.out


def test_create_without_installing_dependencies(
    tmp_path: Path,
    capsys: object,
) -> None:
    result = main(
        [
            "etl-read-csv.py",
            "--project-dir",
            str(tmp_path),
            "--no-install-dependencies",
        ]
    )

    assert result == 0
    assert (tmp_path / "notebooks" / "01-etl-read-csv.py").is_file()
    output = cast(CaptureFixture, capsys).readouterr()
    assert "Template dependencies were not installed" in output.out
