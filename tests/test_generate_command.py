from pathlib import Path
from click.testing import CliRunner
from chartbook.cli import main
import shutil

def test_generate_command(tmp_path, monkeypatch):
    """Test generate command in example directory"""
    # Setup paths
    example_dir = Path("example/to_be_published/EX")
    output_dir = example_dir / "docs"
    
    # Clean previous runs
    if output_dir.exists():
        shutil.rmtree(output_dir)

    # Change to example directory
    monkeypatch.chdir(example_dir)
    print(f"Current directory: {Path.cwd()}")  # Debug directory
    print(f"Directory contents: {[f.name for f in Path.cwd().iterdir()]}")  # Debug files

    # Run the command
    runner = CliRunner()
    result = runner.invoke(main, ["generate", "./docs", "--force-write"])

    # Debug output
    print("Command output:", result.output)
    print("Exception:", result.exception)

    # Check command success
    assert result.exit_code == 0, f"Command failed with output: {result.output}"

    # Verify output file
    html_file = Path("docs/index.html")
    assert html_file.exists(), "HTML output not generated"
    assert html_file.stat().st_size > 0, "HTML file is empty" 