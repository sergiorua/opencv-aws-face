import yaml

class Config:
    config_file = 'config.yaml'
    config = {}

    def __init__(self):
        with open(self.config_file, 'r') as c:
            try:
                self.config = yaml.load(c)
            except:
                raise "Cannot open %s config file" % (self.config_file)