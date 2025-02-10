import importlib.resources
import shutil
import subprocess
from pathlib import Path

from chartbook import pipeline_publish
from chartbook.config import get_logo_path, load_config

TEMP_DOCS_SRC_DIR = Path("_docs_src")


def get_docs_src_path(pipeline_theme: str = "pipeline"):
    """Get the path to the docs_src directory included in the package."""
    package_path = importlib.resources.files("chartbook")
    if pipeline_theme == "pipeline":
        return Path(str(package_path)) / "docs_src_pipeline"
    elif pipeline_theme == "chartbook":
        return Path(str(package_path)) / "docs_src_chartbook"
    else:
        raise ValueError(f"Invalid pipeline theme: {pipeline_theme}")


def run_pipeline_publish(
    project_dir: Path,
    pipeline_dev_mode: bool = False,
    pipeline_theme: str = "chartbook",
    publish_dir: Path = Path("./_output/to_be_published/"),
    _docs_dir: Path = Path("./_docs"),
    docs_src_dir: Path = TEMP_DOCS_SRC_DIR,
):
    """Run the pipeline publish script to generate markdown files.

    Args:
        docs_dir: Directory containing documentation source files
        project_dir: Root directory of the project
        pipeline_dev_mode: Enable pipeline development mode
        pipeline_theme: Theme to use for pipeline documentation
        publish_dir: Directory where files will be published
        _docs_dir: Directory where documentation will be built
    """
    project_dir = Path(project_dir).resolve()
    publish_dir = Path(publish_dir).resolve()
    _docs_dir = Path(_docs_dir).resolve()
    docs_src_dir = Path(docs_src_dir).resolve()

    pipeline_publish.main(
        docs_build_dir=_docs_dir,
        base_dir=project_dir,
        pipeline_dev_mode=pipeline_dev_mode,
        pipeline_theme=pipeline_theme,
        publish_dir=publish_dir,
        docs_src_dir=docs_src_dir,
    )


def run_sphinx_build(_docs_dir: Path):
    """Run sphinx-build to generate HTML files."""
    build_cmd = [
        "sphinx-build",
        "-M",
        "html",
        str(_docs_dir),
        str(_docs_dir / "_build"),
    ]

    result = subprocess.run(build_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Sphinx build failed:\n{result.stderr}")


def generate_docs(
    output_dir: Path,
    project_dir: Path,
    pipeline_dev_mode: bool = False,
    pipeline_theme: str = "chartbook",
    publish_dir: Path = Path("./_output/to_be_published/"),
    _docs_dir: Path = Path("./_docs"),
    keep_build_dirs: bool = False,
    temp_docs_src_dir: Path = TEMP_DOCS_SRC_DIR,
):
    """Generate documentation by running both pipeline publish and sphinx build.

    Args:
        output_dir: Directory where output will be generated
        project_dir: Root directory of the project
        pipeline_dev_mode: Enable pipeline development mode
        pipeline_theme: Theme to use for pipeline documentation
        publish_dir: Directory where files will be published
        _docs_dir: Directory where documentation will be built
        keep_build_dirs: If True, keeps temporary build directory after generation
    """

    output_dir = Path(output_dir).resolve()
    publish_dir = Path(publish_dir).resolve()
    _docs_dir = Path(_docs_dir).resolve()
    temp_docs_src_dir = Path(temp_docs_src_dir).resolve()

    # Load configuration
    config = load_config(project_dir)

    # Create temporary build directory
    temp_docs_src_dir.mkdir(exist_ok=True)

    try:
        # Select the correct docs_src directory based on the pipeline theme
        if pipeline_theme == "pipeline":
            _retrieve_correct_docs_src_dir(
                temp_docs_src_dir, config, project_dir, pipeline_theme
            )
        elif pipeline_theme == "chartbook":
            _retrieve_correct_docs_src_dir(
                temp_docs_src_dir, config, project_dir, pipeline_theme
            )
        else:
            raise ValueError(f"Invalid pipeline theme: {pipeline_theme}")

        # Run pipeline publish
        run_pipeline_publish(
            project_dir=project_dir,
            pipeline_dev_mode=pipeline_dev_mode,
            pipeline_theme=pipeline_theme,
            publish_dir=publish_dir,
            _docs_dir=_docs_dir,
            docs_src_dir=temp_docs_src_dir,
        )

        # Update conf.py
        conf_path = temp_docs_src_dir / "conf.py"
        with open(conf_path, "r") as f:
            conf_content = f.read()

        # Update configuration values
        sphinx_theme = {
            "chartbook": "pydata_sphinx_theme",
            "pipeline": "sphinx_book_theme",
        }[pipeline_theme]
        replacements = {
            'project = "ChartBook"': f'project = "{config["site"]["title"]}"',
            'copyright = "2024, Jeremiah Bejarano"': f'copyright = "{config["site"]["copyright"]}, {config["site"]["author"]}"',
            'author = "Jeremiah Bejarano"': f'author = "{config["site"]["author"]}"',
            'html_logo = "../assets/logo.svg"': 'html_logo = "_static/logo.png"',
            'html_favicon = "../assets/logo.svg"': 'html_favicon = "_static/logo.png"',
            'html_theme = "pydata_sphinx_theme"': f'html_theme = "{sphinx_theme}"',
        }

        for old, new in replacements.items():
            conf_content = conf_content.replace(old, new)

        with open(conf_path, "w") as f:
            f.write(conf_content)

        # Run sphinx build
        run_sphinx_build(_docs_dir)

        # Copy build files to output
        output_dir.mkdir(parents=True, exist_ok=True)
        html_build_dir = _docs_dir / "_build" / "html"
        if html_build_dir.exists():
            shutil.copytree(html_build_dir, output_dir, dirs_exist_ok=True)
            # create empty file called .nojekyll for use with github pages
            (output_dir / ".nojekyll").touch()
    finally:
        if not keep_build_dirs:
            # Clean up temporary directory if keep_build_dir is False
            shutil.rmtree(_docs_dir, ignore_errors=True)
            shutil.rmtree(temp_docs_src_dir, ignore_errors=True)
        else:
            print(f"Keeping temporary build directory: {_docs_dir.resolve()}")


def _retrieve_correct_docs_src_dir(
    temp_docs_src_dir: Path,
    config: dict,
    project_dir: Path,
    pipeline_theme: str = "pipeline",
):
    """Copy documentation source files and setup directory structure."""
    # Copy package docs_src contents
    docs_src_path = get_docs_src_path(pipeline_theme)
    for item in docs_src_path.glob("*"):
        if item.is_file():
            shutil.copy2(item, temp_docs_src_dir)
        elif item.is_dir():
            shutil.copytree(item, temp_docs_src_dir / item.name, dirs_exist_ok=True)

    # Create required directories
    (temp_docs_src_dir / "_static").mkdir(exist_ok=True)
    (temp_docs_src_dir / "assets").mkdir(exist_ok=True)

    # Copy logo to both directories
    logo_path = get_logo_path(config, project_dir)
    for dest_dir in ["_static", "assets"]:
        shutil.copy2(logo_path, temp_docs_src_dir / dest_dir / "logo.png")
