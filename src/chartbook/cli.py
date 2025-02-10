import shutil
from pathlib import Path

import click

from chartbook.config import create_config_interactive
from chartbook.generator import generate_docs


@click.group()
def main():
    """ChartBook CLI tool for generating documentation websites."""
    pass


@main.command()
@click.argument("output_dir", type=click.Path(), default="./docs", required=False)
@click.option(
    "--project-dir", "-f", type=click.Path(), help="Path to project directory"
)
@click.option(
    "--pipeline-dev-mode",
    is_flag=True,
    default=False,
    help="Enable pipeline development mode",
)
@click.option(
    "--pipeline-theme",
    default="pipeline",
    help="Theme to use for pipeline documentation",
)
@click.option(
    "--publish-dir",
    type=click.Path(),
    default="./_output/to_be_published/",
    help="Directory where files will be published",
)
@click.option(
    "--docs-build-dir",
    type=click.Path(),
    default="./_docs",
    help="Directory where documentation will be built",
)
@click.option(
    "--temp-docs-src-dir",
    type=click.Path(),
    default="./_docs_src",
    help="Directory where documentation source files are temporarily stored in two stage procedure",
)
@click.option(
    "--keep-build-dirs",
    is_flag=True,
    default=False,
    help="Keep temporary build directory after generation",
)
@click.option(
    "--force-write",
    "-f",
    is_flag=True,
    default=False,
    help="Overwrite existing output directory by deleting it first",
)
def generate(
    output_dir,
    project_dir,
    pipeline_dev_mode,
    pipeline_theme,
    publish_dir,
    docs_build_dir,
    temp_docs_src_dir,
    keep_build_dirs,
    force_write,
):
    """Generate HTML documentation in the specified output directory."""

    # Convert output_dir to Path
    output_dir = Path(output_dir).resolve()

    # Prevent deleting the current working directory
    if output_dir == Path.cwd():
        raise click.UsageError(
            "Output directory cannot be the current directory '.' to prevent accidental project deletion"
        )

    # If the output directory exists, delete it if the --force-write flag is provided
    if output_dir.exists():
        if force_write:
            shutil.rmtree(output_dir)
        else:
            if any(output_dir.iterdir()):
                raise click.UsageError(
                    f"Output directory '{output_dir}' already exists and is not empty. "
                    "Please delete it manually or use the --force-write flag to remove it."
                )

    # If project_dir not provided, use current directory
    if project_dir is None:
        project_dir = Path.cwd()
    else:
        project_dir = Path(project_dir).resolve()

    # Check for config file and create if needed
    config_path = project_dir / "chartbook.toml"
    if not config_path.exists():
        if click.confirm(
            "A chartbook.toml file was not found. Create one now?", default=True
        ):
            create_config_interactive(project_dir)
        else:
            click.echo("Using default configuration.")

    generate_docs(
        output_dir=output_dir,
        project_dir=project_dir,
        pipeline_dev_mode=pipeline_dev_mode,
        pipeline_theme=pipeline_theme,
        publish_dir=publish_dir,
        _docs_dir=docs_build_dir,
        temp_docs_src_dir=temp_docs_src_dir,
        keep_build_dirs=keep_build_dirs,
    )
    click.echo(f"Successfully generated documentation in {output_dir}")


if __name__ == "__main__":
    main()
