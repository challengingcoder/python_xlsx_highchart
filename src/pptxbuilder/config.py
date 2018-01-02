import configparser as config_parser
import os
import ast

config = config_parser.ConfigParser()
config.optionxform = str

config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config.ini')

if not os.path.isfile(config_file_path):
    raise EnvironmentError('Config file config.ini not exists!')

config.read(config_file_path)


def config_get_section(section):
    all_sections = {s: dict(config.items(s)) for s in config.sections()}
    the_section = all_sections[section]

    for k, v in the_section.items():

        # dictionaries
        if v.startswith('{'):
            the_section[k] = ast.literal_eval(v)

        # booleans
        the_section[k] = True if v == 'True' else v
        the_section[k] = False if v == 'False' else v

    return the_section


def config_get(section, option):
    return config.get(section, option)


def config_get_int(section, option):
    return config.getint(section, option)


def config_get_bool(section, option):
    return config.getboolean(section, option)


if __name__ == '__main__':
    config_val = config_get('DB', 'URI')
    print(config_val)