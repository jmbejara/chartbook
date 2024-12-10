import click
from pathlib import Path
from chartbook.generator import generate_docs

@click.group()
def main():
    """ChartBook CLI tool for generating documentation websites."""
    pass

@main.command()
@click.argument('output_dir', type=click.Path())
@click.option('--project-dir', '-f', type=click.Path(), help='Path to project directory')
@click.option('--pipeline-dev-mode', is_flag=True, default=False,
              help='Enable pipeline development mode')
@click.option('--pipeline-theme', default="chart_book",
              help='Theme to use for pipeline documentation')
@click.option('--publish-dir', type=click.Path(), default="./_output/to_be_published/",
              help='Directory where files will be published')
@click.option('--docs-build-dir', type=click.Path(), default="./_docs",
              help='Directory where documentation will be built')
def generate(output_dir, project_dir, pipeline_dev_mode, pipeline_theme, publish_dir, docs_build_dir):
    """Generate HTML documentation in the specified output directory."""
    
    # If project_dir not provided, use current directory
    if project_dir is None:
        project_dir = Path.cwd()
    else:
        project_dir = Path(project_dir).resolve()

    # Convert string paths to Path objects
    publish_dir = Path(publish_dir).resolve()
    docs_build_dir = Path(docs_build_dir).resolve()

    try:
        generate_docs(
            output_dir=output_dir,
            project_dir=project_dir,
            pipeline_dev_mode=pipeline_dev_mode,
            pipeline_theme=pipeline_theme,
            publish_dir=publish_dir,
            docs_build_dir=docs_build_dir
        )
        click.echo(f"Successfully generated documentation in {output_dir}/_build/html")
    except Exception as e:
        click.echo(f"Error generating documentation: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()