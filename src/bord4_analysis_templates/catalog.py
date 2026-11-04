"""Read and install the templates bundled with this distribution."""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import cast

PACKAGE_NAME = "bord4_analysis_templates"
SAFE_FILE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")


class ManifestError(ValueError):
    """Raised when the bundled template manifest is invalid."""


class TemplateNotFoundError(KeyError):
    """Raised when a requested template is not in the catalog."""


class TemplateExistsError(FileExistsError):
    """Raised when installing a template would overwrite a file."""


@dataclass(frozen=True, slots=True)
class Template:
    """Metadata for one bundled template."""

    name: str
    destination: str
    suggested_name: str
    dependencies: tuple[str, ...]


def _source_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_bundled_text(name: str) -> str:
    packaged = files(PACKAGE_NAME).joinpath(name)
    if packaged.is_file():
        return packaged.read_text(encoding="utf-8")

    source_path = _source_root() / name
    if source_path.is_file():
        return source_path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Bundled resource is missing: {name}")


def _required_string(metadata: dict[str, object], key: str, template: str) -> str:
    value = metadata.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{template}: {key} must be a non-empty string")
    return value.strip()


def _dependencies(metadata: dict[str, object], template: str) -> tuple[str, ...]:
    value = metadata.get("dependencies", [])
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise ManifestError(f"{template}: dependencies must be a list of strings")
    return tuple(cast(str, item).strip() for item in value)


def list_templates() -> tuple[Template, ...]:
    """Return all templates from the bundled manifest, sorted by file name."""
    manifest = tomllib.loads(_read_bundled_text("templates.toml"))
    raw_templates = manifest.get("templates")
    if not isinstance(raw_templates, dict):
        raise ManifestError("templates.toml is missing the [templates] table")

    templates: list[Template] = []
    for name, raw_metadata in raw_templates.items():
        if not isinstance(name, str) or not isinstance(raw_metadata, dict):
            raise ManifestError("Template names and metadata must be TOML tables")
        metadata = cast(dict[str, object], raw_metadata)
        templates.append(
            Template(
                name=name,
                destination=_required_string(metadata, "destination", name),
                suggested_name=_required_string(metadata, "suggested_name", name),
                dependencies=_dependencies(metadata, name),
            )
        )
    return tuple(sorted(templates, key=lambda template: template.name))


def get_template(name: str) -> Template:
    """Return metadata for a template by its exact file name."""
    for template in list_templates():
        if template.name == name:
            return template
    raise TemplateNotFoundError(name)


def read_template(name: str) -> str:
    """Return the source text for a template in the catalog."""
    get_template(name)
    return _read_bundled_text(f"templates/{name}")


def _safe_name(name: str, default_suffix: str) -> str:
    candidate = name.strip()
    if not candidate:
        raise ValueError("File name is required")
    if Path(candidate).name != candidate or not SAFE_FILE_NAME.fullmatch(candidate):
        raise ValueError(
            "File name may only contain letters, numbers, dots, hyphens and underscores"
        )
    if not Path(candidate).suffix:
        candidate = f"{candidate}{default_suffix}"
    return candidate


def copy_template(
    name: str,
    *,
    project_dir: str | Path = ".",
    destination: str | Path | None = None,
    output_name: str | None = None,
) -> Path:
    """Copy a bundled template into a project without overwriting files."""
    output_path = template_path(
        name,
        project_dir=project_dir,
        destination=destination,
        output_name=output_name,
    )
    if output_path.exists():
        raise TemplateExistsError(str(output_path))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(read_template(name), encoding="utf-8")
    return output_path


def template_path(
    name: str,
    *,
    project_dir: str | Path = ".",
    destination: str | Path | None = None,
    output_name: str | None = None,
) -> Path:
    """Resolve where a template would be copied without writing anything."""
    template = get_template(name)
    project_path = Path(project_dir)
    destination_path = Path(destination or template.destination)
    if not destination_path.is_absolute():
        destination_path = project_path / destination_path

    file_name = _safe_name(
        output_name or template.suggested_name,
        "".join(Path(template.name).suffixes),
    )
    return destination_path / file_name
