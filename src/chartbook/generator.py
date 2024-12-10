import shutil
import subprocess
from pathlib import Path

def run_pipeline_publish(docs_dir: Path):
    """Run the pipeline publish script to generate markdown files."""
    # Import here to avoid circular imports
    import pipeline_publish
    
    # Run pipeline publish script
    pipeline_publish.main(docs_build_dir=docs_dir)

def run_sphinx_build(docs_dir: Path):
    """Run sphinx-build to generate HTML files."""
    build_cmd = ["sphinx-build", "-M", "html", str(docs_dir), str(docs_dir / "_build")]
    
    result = subprocess.run(build_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Sphinx build failed:\n{result.stderr}")

def generate_docs(output_dir: Path):
    """Generate documentation by running both pipeline publish and sphinx build."""
    # First run pipeline publish
    run_pipeline_publish(output_dir)
    
    # Then run sphinx build
    run_sphinx_build(output_dir)