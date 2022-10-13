
class Place:

    def __init__(self, nombre, tokens:int):
        self.nombre = nombre
        self.tokens = tokens

    def __str__(self):
        return "Lugar: {},tokens: {} ".format(self.nombre, self.tokens)
    
    def __repr__(self):
        return self.__str__()
    
    def update_tokens(self, tokens: int):
        self.tokens = tokens
    
    
 

class transition1:
    def __init__(self, nombre:str):
        self.nombre = nombre

    def __str__(self):
        return "{}".format(self.nombre)

    def __repr__(self):
        return self.__str__()

class input_transitions():
    def __init__(self, place: str, tokens: int, transitio: str,  weight: int):
        self.place = place
        self.transitio = transitio
        self.weight = weight

    def __repr__(self):
        return "({} -> t: {} w: {})".format(self.place, self.transitio, self.weight)

    def __str__(self):
        return self.__repr__()
    


class out_transitions():
    def __init__(self, transitio: str, place: str, tokens: int, weight: int):
        self.transitio = transitio
        self.place = place
        self.weight = weight
        

    def __repr__(self):
        return "({} -> {}  w: {})".format(self.transitio, self.place,  self.weight)

    def __str__(self):
        return self.__repr__()
    

        