import tomli
import tomli_w
from pathlib import Path
import click
import shutil
import importlib.resources
from datetime import datetime

DEFAULT_CONFIG = {
    "theme": {
        "logo_path": "",
        "favicon_path": "",
    },
    "site": {
        "title": "ChartBook",
        "author": "",
        "copyright": "",
    }
}

def get_default_asset_path(filename: str) -> Path:
    """Get path to default asset from package resources"""
    package_path = importlib.resources.files("chartbook")
    try:
        # First try to get the asset directly using importlib.resources
        with importlib.resources.as_file(package_path / "assets" / filename) as asset_path:
            return Path(str(asset_path))
    except (TypeError, FileNotFoundError):
        # Fallback for development mode
        return Path(str(package_path)).parent / "assets" / filename

def get_template_path(filename: str) -> Path:
    """Get path to template file from package resources"""
    package_path = importlib.resources.files("chartbook")
    return Path(str(package_path)) / "templates" / filename

def load_config(project_dir: Path) -> dict:
    """Load configuration from chartbook.toml"""
    config_path = project_dir / "chartbook.toml"
    
    if not config_path.exists():
        return DEFAULT_CONFIG
        
    with open(config_path, "rb") as f:
        return tomli.load(f)

def create_config_interactive(project_dir: Path) -> dict:
    """Create configuration file interactively"""
    config = DEFAULT_CONFIG.copy()
    
    if click.confirm("Would you like to supply a custom logo?", default=False):
        logo_path = click.prompt(
            "Enter path to logo file (relative to project directory)",
            type=click.Path(exists=True)
        )
        config["theme"]["logo_path"] = str(Path(logo_path))
    
    # Always prompt for site information
    config["site"]["title"] = click.prompt("Site title", default="ChartBook")
    config["site"]["author"] = click.prompt("Author name", default="")
    config["site"]["copyright"] = click.prompt(
        "Copyright",
        default=str(datetime.now().year)
    )
    
    # Save config
    config_path = project_dir / "chartbook.toml"
    with open(config_path, "wb") as f:
        tomli_w.dump(config, f)
    
    return config

def get_logo_path(config: dict, project_dir: Path) -> Path:
    """Get logo path from config or return default"""
    if config["theme"]["logo_path"]:
        return project_dir / config["theme"]["logo_path"]
    return get_default_asset_path("logo.png")