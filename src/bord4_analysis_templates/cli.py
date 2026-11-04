"""Command-line interface for installing templates into an analysis project."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from bord4_analysis_templates.catalog import (
    ManifestError,
    Template,
    TemplateExistsError,
    TemplateNotFoundError,
    copy_template,
    get_template,
    list_templates,
    template_path,
)


def _print_templates(templates: tuple[Template, ...]) -> None:
    for template in templates:
        print(f"{template.name} -> {template.destination}/{template.suggested_name}")
        if template.dependencies:
            print(f"  dependencies: {', '.join(template.dependencies)}")


def _choose_template(templates: tuple[Template, ...]) -> str:
    print("Velg template:")
    for index, template in enumerate(templates, start=1):
        print(f"  {index}. {template.name}")

    while True:
        answer = input("> ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(templates):
            return templates[int(answer) - 1].name
        if any(template.name == answer for template in templates):
            return answer
        print("Velg et nummer fra listen.")


def _install_dependencies(dependencies: tuple[str, ...], project_dir: Path) -> None:
    if not dependencies:
        return
    print("Adding template dependencies to the project:")
    for dependency in dependencies:
        print(f"  {dependency}")
    subprocess.run(
        ["uv", "add", *dependencies],
        cwd=project_dir,
        check=True,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a local file from bord4-analysis-templates.",
    )
    parser.add_argument("template_name", nargs="?")
    parser.add_argument("--template", dest="template_option")
    parser.add_argument("--destination")
    parser.add_argument("--name")
    parser.add_argument("--project-dir", default=".")
    parser.add_argument("--list", action="store_true", help="List templates and exit.")
    parser.add_argument(
        "--no-install-dependencies",
        action="store_true",
        help="Create the file without adding dependencies with uv.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the template installer."""
    args = _parser().parse_args(argv)
    try:
        templates = list_templates()
        if args.list:
            _print_templates(templates)
            return 0

        name = args.template_option or args.template_name or _choose_template(templates)
        template = get_template(name)
        project_dir = Path(args.project_dir).resolve()

        # Detect output conflicts before uv modifies the project.
        expected_path = template_path(
            name,
            project_dir=project_dir,
            destination=args.destination,
            output_name=args.name,
        )
        if expected_path.exists():
            raise TemplateExistsError(str(expected_path))

        if not args.no_install_dependencies:
            _install_dependencies(template.dependencies, project_dir)

        output_path = copy_template(
            name,
            project_dir=project_dir,
            destination=args.destination,
            output_name=args.name,
        )
    except (
        FileNotFoundError,
        ManifestError,
        subprocess.CalledProcessError,
        TemplateExistsError,
        TemplateNotFoundError,
        ValueError,
    ) as error:
        print(f"Klarte ikke å opprette template: {error}", file=sys.stderr)
        return 1

    print(f"Created {output_path} from {name}")
    if args.no_install_dependencies and template.dependencies:
        print("Template dependencies were not installed:")
        for dependency in template.dependencies:
            print(f"  {dependency}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
