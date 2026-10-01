class Config:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.app_name = "My Application"
            cls.instance.language = "English"
        return cls.instance

config1 = Config()
config2 = Config()
config1.language = "Spanish"
print(config2.app_name)
print(config2.language)
print(config1.language)
print(config1 is config2)
