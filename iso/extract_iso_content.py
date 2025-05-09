import pathlib
import subprocess

from iso.clean import clean


def mount_iso(iso_path: pathlib.Path, iso_mnt: pathlib.Path) -> bool:
    try:
        subprocess.run(
            f"mount -o loop {iso_path} {iso_mnt}",
            capture_output=True,
            check=True,
            text=True,
            shell=True,
        )

        print("Successfully mounted ISO")

        return True
    except subprocess.CalledProcessError:
        print("Failed to mount ISO")
        return False


def umount_iso(iso_mnt: pathlib.Path) -> bool:
    try:
        subprocess.run(
            f"umount {iso_mnt}",
            capture_output=True,
            check=True,
            text=True,
            shell=True,
        )

        print("Successfully unmounted ISO")

        return True
    except subprocess.CalledProcessError:
        print("Failed to unmount ISO")
        return False


def extract_iso_content(iso_path: pathlib.Path, iso_mnt: pathlib.Path, iso_content_dir: pathlib.Path):
    result = mount_iso(iso_path, iso_mnt)

    if not result:
        clean()
        exit(1)

    print("Extracting ISO content")

    try:
        subprocess.run(
            f"rsync -avz --no-owner --no-group {iso_mnt}/ {iso_content_dir}",
            capture_output=True,
            check=True,
            text=True,
            shell=True,
        )

        print("Successfully extracted ISO content")

    except subprocess.CalledProcessError:
        print("Failed to extract ISO content")
        clean()
        exit(1)

    result = umount_iso(iso_mnt)

    if not result:
        clean()
        exit(1)
