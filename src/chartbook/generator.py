import subprocess
from pathlib import Path
import importlib.resources
import shutil


def get_docs_src_path():
    """Get the path to the docs_src directory included in the package."""
    package_path = importlib.resources.files("chartbook")
    return Path(str(package_path)).parent.parent / "docs_src"


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
):
    """Generate documentation by running both pipeline publish and sphinx build.

    Args:
        output_dir: Directory where final HTML documentation will be output
        project_dir: Root directory of the project
        pipeline_dev_mode: Enable pipeline development mode
        pipeline_theme: Theme to use for pipeline documentation
        publish_dir: Directory where files will be published
        docs_build_dir: Directory where documentation will be built
    """
    output_dir = Path(output_dir).resolve()
    publish_dir = Path(publish_dir).resolve()
    docs_build_dir = Path(docs_build_dir).resolve()

    # Create temporary build directory
    temp_dir = Path("._chart_book_temp")
    temp_dir.mkdir(exist_ok=True)

    try:
        # Run pipeline publish with temporary directory
        run_pipeline_publish(
            docs_dir=temp_dir,
            project_dir=project_dir,
            pipeline_dev_mode=pipeline_dev_mode,
            pipeline_theme=pipeline_theme,
            publish_dir=publish_dir,
            docs_build_dir=docs_build_dir,
        )

        # Run sphinx build in temporary directory
        run_sphinx_build(temp_dir)

        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Copy only the HTML build files to the final output directory
        html_build_dir = temp_dir / "_build" / "html"
        if html_build_dir.exists():
            # Remove existing files in output directory
            if output_dir.exists():
                shutil.rmtree(output_dir)
            # Copy HTML files to output directory
            shutil.copytree(html_build_dir, output_dir)
    finally:
        # Clean up temporary directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
