import click
from pathlib import Path
from chartbook.generator import generate_docs
from chartbook.config import load_config, create_config_interactive


@click.group()
def main():
    """ChartBook CLI tool for generating documentation websites."""
    pass


@main.command()
@click.argument("output_dir", type=click.Path())
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
    default="chartbook",
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
    "--keep-build-dir",
    is_flag=True,
    default=False,
    help="Keep temporary build directory after generation",
)
def generate(
    output_dir,
    project_dir,
    pipeline_dev_mode,
    pipeline_theme,
    publish_dir,
    docs_build_dir,
    keep_build_dir,
):
    """Generate HTML documentation in the specified output directory."""

    # Convert output_dir to Path
    output_dir = Path(output_dir).resolve()
    
    # Safety checks for output directory
    if output_dir == Path.cwd():
        raise click.UsageError("Output directory cannot be the current directory '.' to prevent accidental project deletion")
    
    if output_dir.exists():
        # Check if directory is empty
        if any(output_dir.iterdir()):
            raise click.UsageError(
                f"Output directory '{output_dir}' already exists and is not empty. "
                "Please delete it manually if you want to regenerate documentation."
            )

    # If project_dir not provided, use current directory
    if project_dir is None:
        project_dir = Path.cwd()
    else:
        project_dir = Path(project_dir).resolve()

    # Check for config file and create if needed
    config_path = project_dir / "chartbook.toml"
    if not config_path.exists():
        if click.confirm("A chartbook.toml file was not found. Create one now?", default=True):
            create_config_interactive(project_dir)
        else:
            click.echo("Using default configuration.")

    try:
        generate_docs(
            output_dir=output_dir,
            project_dir=project_dir,
            pipeline_dev_mode=pipeline_dev_mode,
            pipeline_theme=pipeline_theme,
            publish_dir=publish_dir,
            docs_build_dir=docs_build_dir,
            keep_build_dir=keep_build_dir,
        )
        click.echo(f"Successfully generated documentation in {output_dir}")
    except Exception as e:
        click.echo(f"Error generating documentation: {str(e)}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()
