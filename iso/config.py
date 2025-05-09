import pathlib


class IsoConfig:
    def __init__(self, include_images: bool, images: list[str] = None, server_config_name: bool = True):
        self.__include_images = include_images

        self.__images = images if images is not None else []

        self.__server_url: str | None = None
        self.__configuration_script_name: str | None = None
        self.__iourc_configuration_file: pathlib.Path | None = None

        self.__custom_project_name = input("Enter the project name (without spaces): ")
        self.__custom_project_name = self.__custom_project_name.replace(" ", "_")

        include_iourc_creation_script = True if input(
            "Do you want to include the creation of the iourc configuration file in the script? (y/n) ") == "y" else False

        if include_iourc_creation_script:
            self.__iourc_configuration_file = pathlib.Path("./default_scripts/create_iourc_file.py")

        if not self.__include_images:
            self.__server_url = input("Enter the server URL: ")
            if server_config_name:
                self.__configuration_script_name = input("Enter the server configuration script name: ")

    @property
    def include_images(self) -> bool:
        return self.__include_images

    @include_images.setter
    def include_images(self, value: bool):
        self.__include_images = value

    @property
    def images(self) -> list[str]:
        return self.__images

    @property
    def server_url(self) -> str | None:
        return self.__server_url

    @property
    def configuration_script_name(self) -> str | None:
        return self.__configuration_script_name

    @configuration_script_name.setter
    def configuration_script_name(self, value: str):
        self.__configuration_script_name = value

    @property
    def iourc_configuration_file(self) -> pathlib.Path | None:
        return self.__iourc_configuration_file

    @property
    def custom_project_name(self) -> str:
        return self.__custom_project_name
