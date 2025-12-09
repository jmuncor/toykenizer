
class Tokenizer:
    """
    Base class for ever tokenizer.    
    """

    def __init__(self):
        self.vocab = {}

    def encode(self, text:str) => list[int]:
        return [1,2,3]

    def decode(self, ids:list[int]) => str:
        return "Decoded String"
