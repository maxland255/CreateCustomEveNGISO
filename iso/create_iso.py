import pathlib
import subprocess

from iso.config import IsoConfig


def create_iso(config: IsoConfig, output_iso_path: pathlib.Path):
    print("Creating ISO")

    try:
        result = subprocess.run(
            f"sudo xorriso -as mkisofs -r -J -joliet-long -V \"{config.custom_project_name}\" -o {output_iso_path} -b boot/grub/i386-pc/eltorito.img -no-emul-boot -boot-load-size 4 -boot-info-table iso_content",
            capture_output=True,
            shell=True,
            check=True,
            text=True,
        )

        print(result.stdout)

        print("ISO created")

    except subprocess.CalledProcessError as e:
        print(e.stdout)

        print(e.stderr)

        print("Error creating the ISO")
