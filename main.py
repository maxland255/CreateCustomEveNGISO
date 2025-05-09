import argparse
import pathlib
import shutil

from image.image_creator import create_image
from iso.config import IsoConfig
from iso.configure_user_data import update_user_data_file
from iso.copy_all_file import copy_all_file_in_iso
from iso.create_iso import create_iso
from iso.create_script import create_client_script, create_server_script
from iso.setup_iso_project import setup_iso_project
from iso.extract_iso_content import extract_iso_content
from iso.update_eve_ng_script import update_eve_ng_script
from iso.update_grub_cfg import update_grub_cfg


def main():
    parser = argparse.ArgumentParser(description="A simple program to personalize an Eve-NG ISO installer.")

    # Add argument to choose to create a new ISO or create an image for eve-ng

    parser.add_argument("mode", choices=["iso", "image", "server"], help="Choose the mode to create the ISO, the image or server configuration script")

    parser.add_argument("-i", "--iso_path", help="Path to the original ISO file")
    parser.add_argument("-o", "--output_path", help="Path to the output iso file")

    # iso arguments
    parser.add_argument("-l", "--image_list", nargs="+", help="Dynamips, Iol and Qemu images list")
    parser.add_argument("--include-images", help="Include images in the ISO", action="store_true")

    # image arguments
    parser.add_argument("-p", "--path", help="Path to the image")
    parser.add_argument("-n", "--name", help="Name of the image")
    parser.add_argument("-t", "--type", choices=["dynamips", "iol", "qemu"], help="Type of the image")

    args = parser.parse_args()

    # Check if the mode is iso and if the iso_path and output_path are provided
    if args.mode == "iso":
        if args.iso_path and args.output_path:
            if (args.image_list and not args.include_images) or (not args.image_list and args.include_images):
                print("Error: --image-list is required")
                exit(1)

            print("Creating an ISO")

            images_path_list: list[pathlib.Path] = [pathlib.Path(img) for img in args.image_list] if args.image_list is not None else []
            images_name_list: list[str] = [img.name for img in images_path_list]

            if args.include_images:
                for img in images_path_list:
                    if not img.exists():
                        print(f"The image {img} does not exist")
                        exit(1)

            iso_path = pathlib.Path(args.iso_path)
            output_iso_path = pathlib.Path(args.output_path)

            if not iso_path.exists():
                print("The ISO path does not exist")
                exit(1)

            if output_iso_path.exists():
                print("The output ISO path already exists")
                exit(1)

            iso_content_dir, iso_mnt_dir, script_dir = setup_iso_project()

            extract_iso_content(iso_path, iso_mnt_dir, iso_content_dir)

            config = IsoConfig(args.include_images, images_name_list)

            if not config.include_images:
                create_client_script(config, script_dir)
            else:
                create_server_script(config, script_dir)

            update_user_data_file(config)

            copy_all_file_in_iso(config, script_dir)

            update_eve_ng_script()

            update_grub_cfg(config)

            create_iso(config, output_iso_path)
        else:
            print("You need to provide the path to the original ISO and the path to the output ISO")
            exit(1)

    elif args.mode == "image":
        if args.path and args.name and args.type:
            print("Creating an image")
            create_image(args.path, args.name, args.type)
        else:
            print("You need to provide the path to the image, the name of the image and the type of the image")
            exit(1)

    elif args.mode == "server":
        if not args.image_list:
            print("You need to provide the images list")
            exit(1)

        print("Creating a server configuration script")

        config = IsoConfig(False, args.image_list, server_config_name=False)

        create_server_script(config, pathlib.Path("."))

        print(f"Server configuration script created at {pathlib.Path('.') / f'{config.custom_project_name}.sh'}")

        if config.iourc_configuration_file is not None:
            print("Export create_iourc_file.py...")

            shutil.copy("./default_scripts/create_iourc_file.py", ".")

            print("Export create_iourc_file.py done")

        # Add a message to place the script in the server to get access with the server url + script name
        print(f"\nPlace the {config.custom_project_name}.sh script in the server to get access with the server {config.server_url}/{config.custom_project_name}.sh\n")
        if config.iourc_configuration_file is not None:
            print(f"\nPlace the create_iourc_file.py script in the server to get access with the server {config.server_url}/create_iourc_file.py\n")
    else:
        print("You need to provide the mode")
        exit(1)


if __name__ == '__main__':
    main()
