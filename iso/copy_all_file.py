import os
import pathlib
import shutil
import subprocess

from iso.config import IsoConfig


def copy_all_file_in_iso(config: IsoConfig, script_dir: pathlib.Path):
    print("Copying all files in the ISO")

    # Copy the server script
    script_file = script_dir / f"{config.custom_project_name}.sh"

    shutil.copy(script_file, f"iso_content/server/{config.custom_project_name}.sh")

    subprocess.run(
        "chmod +x iso_content/server/*.sh",
        shell=True,
    )

    if config.include_images:
        # Copy the images
        os.mkdir("iso_content/server/images")

        for image in config.images_path:
            shutil.copy(image, f"iso_content/server/images/{image.name}")

        if config.iourc_configuration_file is not None:
            shutil.copy(config.iourc_configuration_file, "iso_content/server/create_iourc_file.py")

    print("Finished copying all files in the ISO")
