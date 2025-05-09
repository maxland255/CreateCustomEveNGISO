import pathlib


def setup_iso_project() -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    print("Setup the ISO project")

    project_dir = pathlib.Path(".")

    project_dir.mkdir(parents=True, exist_ok=True)

    iso_content_dir = project_dir / "iso_content"
    iso_mnt_dir = project_dir / "iso_mnt"
    scripts_dir = project_dir / "scripts"

    iso_content_dir.mkdir(parents=True, exist_ok=True)
    iso_mnt_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)

    print("Directories created")

    return iso_content_dir, iso_mnt_dir, scripts_dir
