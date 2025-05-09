import pathlib


def update_eve_ng_script():
    print("Updating Eve NG script")

    # Remove the reboot command in eve-setup.sh script

    eve_setup_script = pathlib.Path("iso_content/server/eve-setup.sh")

    with eve_setup_script.open("r") as f:
        lines = f.readlines()

    with eve_setup_script.open("w") as f:
        for line in lines:
            if "reboot" not in line:
                f.write(line)

    print("Eve NG script updated")
