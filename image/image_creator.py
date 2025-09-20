import shutil
import pathlib
import subprocess


DYNAMIPS_PATH = "/opt/unetlab/addons/dynamips"
IOL_PATH = "/opt/unetlab/addons/iol/bin"
QEMU_PATH = "/opt/unetlab/addons/qemu"


def create_image(path: str, name: str, image_type: str):
    print("Creating an image for Eve-NG")

    image_path = pathlib.Path(path)
    image_name = name.replace(" ", "_")

    folder_path = pathlib.Path(f"./{image_name}")

    if not image_path.exists():
        print("The image path does not exist")
        return

    if folder_path.exists():
        print("The folder already exists")
        return

    if image_type not in ["dynamips", "iol", "qemu"]:
        print("Invalid image type")
        return

    print(f"Creating image {image_name} of type {image_type} at {image_path}")

    # Create the image

    if image_type == "qemu":
        install_path = QEMU_PATH + "/" + image_name.replace(" ", "_")
    elif image_type == "iol":
        install_path = IOL_PATH + "/"
    else:
        install_path = DYNAMIPS_PATH + "/"

    image_file_name = image_path.name

    bash_script = ('#!/bin/bash\n'
                   'TMP_DIR=$1\n'
                   f'echo "Installation de l\'image {image_name}..."\n'
                   f'mkdir -p {install_path}\n' if image_type == "qemu" else ''
                   f'mv $TMP_DIR/{image_file_name} {install_path}\n' if image_type != "qemu" else f'mv $TMP_DIR/{image_file_name} {install_path}/virtio.qcow2'
                   f'echo "L\'installation de l\'image {image_name} s\'est terminé avec succès."\n')

    folder_path.mkdir(parents=True, exist_ok=False)

    with open(folder_path / "install.sh", "w") as f:
        f.write(bash_script)

    shutil.copy(image_path, folder_path / image_file_name)

    result = subprocess.run(f"tar czvf {image_name}.tar.gz {image_name}", shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stderr)
        return
    else:
        print(result.stdout)

    shutil.rmtree(folder_path)

    print(f"Image {image_name} created successfully at {folder_path}")
