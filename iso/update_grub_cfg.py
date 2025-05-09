import pathlib

from iso.config import IsoConfig


def update_grub_cfg(config: IsoConfig):
    print("Updating grub config")

    # Update the grub.cfg file to edit the boot menu of the ISO

    grub_cfg_file = pathlib.Path("iso_content/boot/grub/grub.cfg")

    with grub_cfg_file.open("r") as f:
        lines = f.readlines()

    new_grub_menuentry_title = f"Install {config.custom_project_name.replace('_', ' ').replace('-', ' ').title()} EVE-NG"

    with grub_cfg_file.open("w") as f:
        for line in lines:
            if "menuentry" in line and "BM" not in line:
                f.write(f"menuentry \"{new_grub_menuentry_title}\" {{")
            else:
                f.write(line)

    print("Grub config updated")
