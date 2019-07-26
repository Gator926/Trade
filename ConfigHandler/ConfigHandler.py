import configparser


class ConfigHandler:
    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read('/root/Trade/config.ini')
        # self.config_parser.read('../config.ini')

    def get_config_value(self, group_name, name):
        return self.config_parser.get(group_name, name)


if __name__ == '__main__':
    config_handler = ConfigHandler()
    print(config_handler.get_config_value('config', 'password'))
