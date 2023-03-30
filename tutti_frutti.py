import random

class TuttiFrutti:
    def __init__(self,jugadores=['Luisma','Sofi'],rondas=2,cant_jugadores=2,n_cat=2):
        self.cant_jugadores = cant_jugadores
        self.rondas = rondas
        self.partida = {}
        self.tabla = {}
        self.categorias_pret = ["animales",  "paises",   "Nombres",    "peliculas",
                                "series",    "ropa",     "deportes",   "peces",
                                "mamiferos", "reptiles", "aves",       "adjetivos",
                                "verbos",    "colores",  "comida",     "bebida"]
        
        self.crear_tablas(jugadores,n_cat)
        
        
    def crear_tablas(self,jugadores,n_cat):
        for jugador in jugadores:
            self.partida[jugador] = {}
        new_cat = ''
        for col in range(n_cat):
            while new_cat == '' or new_cat in self.tabla.keys():
                new_cat = random.choice(self.categorias_pret)
            self.tabla[new_cat] = []
            for jugador in jugadores:
                self.partida[jugador][new_cat] = []
    
    
    
    def elegir_letra(self):
        num_letra = random.randint(0, 25)
        letra = chr(num_letra + ord('A'))
        return letra

    def agregar_palabra(self,jugador, categoria, palabra):
        self.partida[jugador][categoria].append(palabra)
        
        
        
    def seleccionar_categoria(self,jugador,ronda):
        print("Seleccione una categoría disponible:")
        categorias_disponibles = []
        n = 0
        for categoria in list(self.tabla.keys()):
            if len(self.partida[jugador][categoria]) == ronda:
                n += 1
                print(f"{n}. {categoria}")
                categorias_disponibles.append(categoria)
                
        if len(categorias_disponibles) == 1:
            return categorias_disponibles[0]
        
        cat_num = int(input())
        while cat_num not in range(1, len(categorias_disponibles) + 1):
            print("Opción inválida. Seleccione una categoría disponible:")
            cat_num = int(input())
        return categorias_disponibles[cat_num-1]



    def pedir_palabra(self,jugador,letra_actual,cat_disp):
        print(f"\nIngrese una palabra para la letra {letra_actual} en la categoria {cat_disp}:\n")
        palabra = input()
        while palabra[0].upper() != letra_actual:
            print("ERROR: La palabra ingresada no empieza con la letra " + letra_actual + ". Intentelo nuevamente.\n")
            palabra = input()
        self.agregar_palabra(jugador,cat_disp, palabra)

    
    
    def calcular_puntos(self):
        pass
        
        
    
    def resultado_final(self):
        fila = ''.center(13+(23*len(self.tabla.keys())),"-")
        print("Tutti Frutti\n\n")
        print("\nResultado:\n")
        claves = list(self.tabla.keys())
        for jugador in list(self.partida.keys()):
            print(fila)
            print(jugador.center(13+(23*len(self.tabla.keys()))))
            print(fila)
            print("|","Ronda".center(10),end="|")
            for cat in claves:  #Encabezado de la tabla
                print("|",cat.center(20),end="|")
            print("\n")
            i = 0
            for ronda in range(self.rondas):
                print("|",str(ronda+1).center(10),end="|")
                for palabra in claves:
                    try:
                        print("|",self.partida[jugador][palabra][i].center(20),end="|")
                    except:
                        print("|","-".center(20),end="|")
                print("\n")
                i += 1
            print(fila,"\n\n")



    def jugar(self):
        print("Tutti Frutti\n\n")
        print("Las Categorías para esta partida son:\n")
        for categoria in self.tabla:
            print(f"- {categoria}\n")
            
        # a = str(input("empezamos?"))
        
        for ronda in range(self.rondas):
            letra_actual = self.elegir_letra()
            print("La letra de esta ronda es:"+letra_actual+"\n")
            
            for categoria in self.tabla:
                for jugador in list(self.partida.keys()):
                    print(f"{jugador} te toca!")
                    # Solicitar palabras del usuario
                    cat_disp = self.seleccionar_categoria(jugador,ronda)
                    self.pedir_palabra(jugador,letra_actual,cat_disp)
                    print(self.tabla)
                    print(self.partida)
                    self.resultado_final()
        print("Fin del juego!")
        

if __name__ == '__main__':
    tf = TuttiFrutti()
    tf.jugar()