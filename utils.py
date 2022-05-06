import yaml


def read_config(config_file):
    with open(config_file, "rt", encoding="utf-8") as fi:
        config = yaml.safe_load(fi)
    return config


Config = read_config("config.yml")