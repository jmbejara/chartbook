import subprocess
from pathlib import Path
import importlib.resources
import shutil


def get_docs_src_path():
    """Get the path to the docs_src directory included in the package."""
    package_path = importlib.resources.files("chartbook")
    return Path(str(package_path)) / "docs_src"


def run_pipeline_publish(
    docs_dir: Path,
    project_dir: Path,
    pipeline_dev_mode: bool = False,
    pipeline_theme: str = "chartbook",
    publish_dir: Path = Path("./_output/to_be_published/"),
    docs_build_dir: Path = Path("./_docs"),
):
    """Run the pipeline publish script to generate markdown files.

    Args:
        docs_dir: Directory containing documentation source files
        project_dir: Root directory of the project
        pipeline_dev_mode: Enable pipeline development mode
        pipeline_theme: Theme to use for pipeline documentation
        publish_dir: Directory where files will be published
        docs_build_dir: Directory where documentation will be built
    """
    from chartbook import pipeline_publish

    pipeline_publish.main(
        docs_build_dir=docs_dir,
        base_dir=project_dir,
        pipeline_dev_mode=pipeline_dev_mode,
        pipeline_theme=pipeline_theme,
        publish_dir=publish_dir,
    )


def run_sphinx_build(docs_dir: Path):
    """Run sphinx-build to generate HTML files."""
    build_cmd = ["sphinx-build", "-M", "html", str(docs_dir), str(docs_dir / "_build")]

    result = subprocess.run(build_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Sphinx build failed:\n{result.stderr}")


def generate_docs(
    output_dir: Path,
    project_dir: Path,
    pipeline_dev_mode: bool = False,
    pipeline_theme: str = "chartbook",
    publish_dir: Path = Path("./_output/to_be_published/"),
    docs_build_dir: Path = Path("./_docs"),
    keep_build_dir: bool = False,
):
    """Generate documentation by running both pipeline publish and sphinx build.
    
    Args:
        output_dir: Directory where output will be generated
        project_dir: Root directory of the project
        pipeline_dev_mode: Enable pipeline development mode
        pipeline_theme: Theme to use for pipeline documentation
        publish_dir: Directory where files will be published
        docs_build_dir: Directory where documentation will be built
        keep_build_dir: If True, keeps temporary build directory after generation
    """
    from chartbook.config import load_config, get_logo_path
    from chartbook.generator import get_docs_src_path
    
    output_dir = Path(output_dir).resolve()
    publish_dir = Path(publish_dir).resolve()
    docs_build_dir = Path(docs_build_dir).resolve()

    # Load configuration
    config = load_config(project_dir)

    # Create temporary build directory
    temp_dir = Path("._chart_book_temp")
    temp_dir.mkdir(exist_ok=True)

    try:
        # Copy all docs_src files to temp directory
        docs_src_path = get_docs_src_path()
        for item in docs_src_path.glob("*"):
            if item.is_file():
                shutil.copy2(item, temp_dir)
            elif item.is_dir():
                shutil.copytree(item, temp_dir / item.name, dirs_exist_ok=True)

        # Create necessary directories
        static_dir = temp_dir / "_static"
        static_dir.mkdir(exist_ok=True)
        
        assets_dir = temp_dir / "assets"
        assets_dir.mkdir(exist_ok=True)

        # Copy logo to both _static and assets directories
        logo_path = get_logo_path(config, project_dir)
        shutil.copy2(logo_path, static_dir / "logo.png")
        shutil.copy2(logo_path, assets_dir / "logo.png")
        
        # Create index.rst if it doesn't exist
        index_rst = temp_dir / "index.rst"
        if not index_rst.exists():
            index_rst.write_text("""
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   index
   dataframes
   charts
   pipelines
""")

        # Run pipeline publish
        run_pipeline_publish(
            docs_dir=temp_dir,
            project_dir=project_dir,
            pipeline_dev_mode=pipeline_dev_mode,
            pipeline_theme=pipeline_theme,
            publish_dir=publish_dir,
            docs_build_dir=docs_build_dir,
        )

        # Update conf.py
        conf_path = temp_dir / "conf.py"
        with open(conf_path, "r") as f:
            conf_content = f.read()

        # Update configuration values
        replacements = {
            'project = "ChartBook"': f'project = "{config["site"]["title"]}"',
            'copyright = "2024, Jeremiah Bejarano"': f'copyright = "{config["site"]["copyright"]}, {config["site"]["author"]}"',
            'author = "Jeremiah Bejarano"': f'author = "{config["site"]["author"]}"',
            'html_logo = "../assets/logo.svg"': 'html_logo = "_static/logo.png"',
            'html_favicon = "../assets/logo.svg"': 'html_favicon = "_static/logo.png"'
        }

        for old, new in replacements.items():
            conf_content = conf_content.replace(old, new)

        with open(conf_path, "w") as f:
            f.write(conf_content)

        # Run sphinx build
        run_sphinx_build(temp_dir)

        # Copy build files to output
        output_dir.mkdir(parents=True, exist_ok=True)
        html_build_dir = temp_dir / "_build" / "html"
        if html_build_dir.exists():
            shutil.copytree(html_build_dir, output_dir, dirs_exist_ok=True)
    finally:
        if not keep_build_dir:
            # Clean up temporary directory if keep_build_dir is False
            shutil.rmtree(temp_dir, ignore_errors=True)
        else:
            print(f"Keeping temporary build directory: {temp_dir.resolve()}")
