import configparser


class ConfigParser(configparser.ConfigParser):
    def get_string(self, section, option, *, raw=False, fallback=None):
        try:
            return self.get(section, option, raw=raw)
        except (configparser.NoOptionError, configparser.NoSectionError):
            return fallback

    def get_int(self, section, option, *, raw=False, fallback=None):
        try:
            return self.getint(section, option, raw=raw)
        except (configparser.NoOptionError, configparser.NoSectionError):
            return fallback

    def get_float(self, section, option, *, raw=False, fallback=None):
        try:
            return self.getfloat(section, option, raw=raw)
        except (configparser.NoOptionError, configparser.NoSectionError):
            return fallback

    def get_boolean(self, section, option, *, raw=False, fallback=None):
        try:
            return self.getboolean(section, option, raw=raw)
        except (configparser.NoOptionError, configparser.NoSectionError):
            return fallback

    def get_list(self, section, option, *, raw=False, fallback=None):
        try:
            value = self.get(section, option, raw=raw)
            if value:
                return [item.strip() for item in value.split(',')]
        except (configparser.NoOptionError, configparser.NoSectionError):
            pass
        return fallback
