

class router():
    """
    Docstring for router
    """
    def __init__(self, name, nb_interfaces):
        self.name=name
        self.nb_int = nb_interfaces
        self.liste_int=[]
        self.protocol_list=[]

    def __str__(self):
        print(f"router name : {self.name} \ninterfaces : {self.nb_int} \nprotocols : {self.protocol_list}")