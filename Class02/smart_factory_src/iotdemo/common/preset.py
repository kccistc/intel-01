"""
ConfigParser helper
"""
from configparser import ConfigParser
from os.path import exists
from re import match

__all__ = ('load_preset', 'save_preset')

__PATTERN = r'^-?\+?\d*(?:\.?\d*)$'


def __to_number(raw_string):
    if match(__PATTERN, raw_string):
        return float(raw_string) if '.' in raw_string else int(raw_string)

    return raw_string


def load_preset(path, key='default'):
    if not exists(path):
        return None

    config = ConfigParser()
    config.read(path)

    if key not in config:
        return None

    data = dict(config[key])
    for key, value in data.items():
        if value[0] in {'[', '{', '('} and value[-1] in {']', '}', ')'}:
            raw = [
                __to_number(val)
                for val in [x.strip() for x in value[1:-1].split(',')]
            ]
            if value[0] == '(':
                data[key] = tuple(raw)
            elif value[0] == '{':
                data[key] = set(raw)
            elif value[0] == '[':
                data[key] = list(raw)
        elif value == 'True':
            data[key] = True
        elif value == 'False':
            data[key] = False
        else:
            data[key] = __to_number(value)

    return data


def save_preset(path, data, key='default', backup=True):
    if data is None:
        return False

    config = ConfigParser()
    if exists(path):
        config.read(path)

    if backup and key in config:
        config[f'_{key}_backup_'] = dict(config[key])

    config[key] = data
    with open(path, 'w') as fp:
        config.write(fp)

    return True
