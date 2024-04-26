class YefClass:
    def __init__(self):
        pass

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__
