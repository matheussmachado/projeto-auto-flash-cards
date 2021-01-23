class MyImageData:
    def __init__(self, bytes , **kwargs):
        self.bytes = bytes
        for k, v in kwargs.items():
            setattr(self, k, v)
