class DataSingleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataSingleton, cls).__new__(cls)

        return cls.instance
