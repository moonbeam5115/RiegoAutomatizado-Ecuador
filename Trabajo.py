
class carro():
    def __init__(self):
        print("Honda")

    def millage(self):
        print("30 km")

    def tanque(self,password):
        print(f"El password es...{password}")
        print(f"El tanque tiene 4 litros")
    
print("Tiempo de riego por Arduino (segundos): ", tiempo)
print("Tiempo de riego por Arduino (minutos): ", tiempo/60)


carro_de_kevin= carro()
carro_de_kevin.millage()
carro_de_kevin.tanque("Goro")
carro_de_tito= carro()
carro_de_tito.millage()
carro_de_tito.tanque("Tito")
