import pathlib

import yaml

from iso.config import IsoConfig


def update_user_data_file(config: IsoConfig):
    print("Updating user data file")

    user_data_file = pathlib.Path("./iso_content/server/user-data")

    with user_data_file.open("r") as f:
        user_data = yaml.safe_load(f)

    autoinstall = user_data["autoinstall"]

    late_commands: list = autoinstall["late-commands"]

    if config.include_images:
        late_commands.insert(2, f"mkdir -p /target/etc/{config.custom_project_name}/")
        late_commands.insert(3, f"cp -rp /cdrom/server/images/* /target/etc/{config.custom_project_name}/")
        late_commands.insert(4, "cp -r /cdrom/server/create_iourc_file.py /target/etc/create_iourc_file.py")

    late_commands.insert(3, f"cp /cdrom/server/{config.custom_project_name}.sh /target/etc/{config.custom_project_name}.sh")

    sub_user_data = autoinstall["user-data"]

    runcmd: list = sub_user_data["runcmd"]

    if not config.include_images:
        runcmd.insert(0, "ip link set ens18 up")
        runcmd.insert(1, "dhclient ens18")

    runcmd.append(f"/etc/{config.custom_project_name}.sh")

    with user_data_file.open("w") as f:
        yaml.dump(user_data, f, sort_keys=False)

    with user_data_file.open("r") as rf:
        file_contents = rf.read()

        file_contents = "#cloud-config\n" + file_contents

    with user_data_file.open("w") as wf:
        wf.write(file_contents)

    print(f"User data file {user_data_file} updated")
