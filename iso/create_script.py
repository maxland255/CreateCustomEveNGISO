import pathlib

from iso.config import IsoConfig


def create_client_script(config: IsoConfig, script_dir: pathlib.Path):
    """
    Create a script included in the ISO to download the server script and execute it.
    :param config:
    :param script_dir:
    :return:
    """

    print("Creating the client script")

    if config.configuration_script_name.endswith(".sh"):
        config.configuration_script_name = config.configuration_script_name[:-3]

    bash_script = ('#!/bin/bash\n'
                   f'SERVER_URL="{config.server_url}"\n'
                   f'TMP_DIR="/tmp/{config.custom_project_name}"\n'
                   f'mkdir -p $TMP_DIR\n'
                   f'echo "Téléchargement du script de configuration d\'Eve-NG..."\n'
                   f'wget "$SERVER_URL/{config.configuration_script_name}.sh" -O "$TMP_DIR/{config.configuration_script_name}.sh"\n'
                   f'chmod +x "$TMP_DIR/{config.configuration_script_name}.sh"\n'
                   f'echo "Exécution du script de configuration d\'Eve-NG..."\n'
                   f'$TMP_DIR/{config.configuration_script_name}.sh $TMP_DIR\n'
                   f'sleep 5\n'
                   f'reboot\n')

    script_file = script_dir / f"{config.custom_project_name}.sh"

    with script_file.open("w") as f:
        f.write(bash_script)

    print(f"Script {script_file} created")


def create_server_script(config: IsoConfig, script_dir: pathlib.Path):
    """
    Create the server script to configure the ISO.
    :param config:
    :param script_dir:
    :return:
    """

    print("Creating the server script")

    bash_script = '#!/bin/bash\n'

    if config.include_images:
        bash_script += (f'TMP_DIR="/tmp/{config.custom_project_name}"\n'
                        f'mkdir -p "$TMP_DIR"\n'
                        f'cp -r /etc/{config.custom_project_name}/* "$TMP_DIR/"\n'
                        f'TAR_FILES=(\n')

        for image in config.images:
            bash_script += f'\t"{image}"\n'

        bash_script += (')\n'
                        'for tar_file in "${TAR_FILES[@]}"; do\n'
                        '\techo "Installation de l\'image $tar_file"\n'
                        '\tfile_url="$TMP_DIR/$tar_file"\n'
                        '\textract_dir="$TMP_DIR/${tar_file%.tar.gz}"\n'
                        '\tmkdir -p "$extract_dir"\n'
                        '\techo "Extraction de l\'archive $tar_file"\n'
                        '\ttar -xzf "$file_url" -C "$TMP_DIR"\n'
                        '\tif [ -f "$extract_dir/install.sh" ]; then\n'
                        '\t\techo "Exécution du script d\'installation de l\'image $tar_file"\n'
                        '\t\tbash "$extract_dir/install.sh" $extract_dir\n'
                        '\telse\n'
                        '\t\techo "Aucun script d\'installation trouvé pour l\'image $tar_file"\n'
                        '\tfi\n'
                        'done\n'
                        'echo "L\'installation des images est terminée"\n')
    else:
        bash_script += (f'SERVER_URL="{config.server_url}"\n'
                        'TMP_DIR=$1\n'
                        f'mkdir -p "$TMP_DIR"\n'
                        f'TAR_FILES=(\n')

        for image in config.images:
            bash_script += f'\t"{image}"\n'

        bash_script += (')\n'
                        'for tar_file in "${TAR_FILES[@]}"; do\n'
                        '\techo "Installation de l\'image $tar_file"\n'
                        '\tfile_url="$SERVER_URL/$tar_file"\n'
                        '\tdest_file="$TMP_DIR/$tar_file"\n'
                        '\textract_dir="$TMP_DIR/${tar_file%.tar.gz}"\n'
                        '\twget "$file_url" -O "$dest_file"\n'
                        '\tmkdir -p "$extract_dir"\n'
                        '\techo "Extraction de l\'archive $tar_file"\n'
                        '\ttar -xzf "$dest_file" -C "$TMP_DIR"\n'
                        '\tif [ -f "$extract_dir/install.sh" ]; then\n'
                        '\t\techo "Exécution du script d\'installation de l\'image $tar_file"\n'
                        '\t\tbash "$extract_dir/install.sh" $extract_dir\n'
                        '\telse\n'
                        '\t\techo "Aucun script d\'installation trouvé pour l\'image $tar_file"\n'
                        '\tfi\n'
                        'done\n'
                        'echo "L\'installation des images est terminée"\n')

    if config.iourc_configuration_file is not None:
        bash_script += 'echo "Configuration du fichier iourc"\n'

        if config.include_images:
            bash_script += ('echo "Exécution du script de création du fichier iourc"\n'
                            'cp /etc/create_iourc_file.py "$TMP_DIR/create_iourc_file.py"\n'
                            'python3 "$TMP_DIR/create_iourc_file.py"\n'
                            'echo "La configuration du fichier iourc est terminée"\n')
        else:
            bash_script += ('echo "Téléchargement du script de création du fichier iourc"\n'
                            'wget "$SERVER_URL/create_iourc_file.py" -O "$TMP_DIR/create_iourc_file.py"\n'
                            'echo "Exécution du script de création du fichier iourc"\n'
                            'python3 "$TMP_DIR/create_iourc_file.py"\n'
                            'echo "La configuration du fichier iourc est terminée"\n')

    bash_script += ('echo "Mise à jour des permissions d\'Eve-NG"\n'
                    '/opt/unetlab/wrappers/unl_wrapper -a fixpermissions\n'
                    'echo "La configuration d\'Eve-NG est terminée"\n')

    if config.include_images:
        bash_script += 'reboot'

    script_file = script_dir / f"{config.custom_project_name}.sh"

    with script_file.open("w") as f:
        f.write(bash_script)

    print(f"Script {script_file} created")
