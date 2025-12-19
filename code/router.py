

class Router():
    """
    Docstring for router
    """
    def __init__(self, name, ID, nb_interfaces):
        self.name = name
        self.ID = ID
        self.nb_int = nb_interfaces
        self.liste_int=[]
        self.protocol_list=[]
        self.AS_name = ""

    def __str__(self):
        print(f"router name : {self.name} (AS {self.AS_name}) \nrouter ID : {self.ID} \ninterfaces : {self.nb_int} \nprotocols : {self.protocol_list}")