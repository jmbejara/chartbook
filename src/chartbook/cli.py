import click
from pathlib import Path
from chartbook.generator import generate_docs

@click.group()
def main():
    """ChartBook CLI tool for generating documentation websites."""
    pass

@main.command()
@click.argument('output_dir', type=click.Path())
def generate(output_dir):
    """Generate HTML documentation in the specified output directory."""
    output_path = Path(output_dir).resolve()

    try:
        generate_docs(output_path)
        click.echo(f"Successfully generated documentation in {output_path}/_build/html")
    except Exception as e:
        click.echo(f"Error generating documentation: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()