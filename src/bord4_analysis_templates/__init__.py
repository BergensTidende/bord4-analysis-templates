"""Versioned analysis templates for Bord4 projects."""

from importlib.metadata import PackageNotFoundError, version

from bord4_analysis_templates.catalog import (
    ManifestError,
    Template,
    TemplateExistsError,
    TemplateNotFoundError,
    copy_template,
    get_template,
    list_templates,
    read_template,
    template_path,
)

try:
    __version__ = version("bord4-analysis-templates")
except PackageNotFoundError:  # pragma: no cover - source tree without installation
    __version__ = "0+unknown"

__all__ = [
    "ManifestError",
    "Template",
    "TemplateExistsError",
    "TemplateNotFoundError",
    "__version__",
    "copy_template",
    "get_template",
    "list_templates",
    "read_template",
    "template_path",
]
