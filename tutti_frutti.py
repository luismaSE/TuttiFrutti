import random

class TuttiFrutti:
    def __init__(self, rondas=3,cant_jugadores=2,n_cat=3):
        self.cant_jugadores = cant_jugadores
        self.rondas = rondas
        self.jugadores = []
        self.categorias = {}
        self.categorias_pret = ["animales",  "paises",   "Nombres",    "peliculas",
                                "series",    "ropa",     "deportes",   "peces",
                                "mamiferos", "reptiles", "aves",       "adjetivos",
                                "verbos",    "colores",  "comida",     "bebida"]
        
        self.elegir_categorias(n_cat)
        self.palabras = {cat: '' for cat in self.categorias.keys()}
        self.esperar_jugador()

        
    def esperar_jugador(self):
        while self.jugadores != self.cant_jugadores:
            print("Esperando a los jugadores...")
            self.jugadores.append(input(f"nombre del jugador{len(self.jugadores)+1}"))
            print(f"Bienvenido {self.jugadores[-1]}")
        print("La partida ya esta llena, empezamos!")
            
        
    def elegir_categorias(self,n_cat):
        new_cat = ''
        for cat in range(n_cat):
            while new_cat == '' or new_cat in self.categorias.keys():
                new_cat = random.choice(self.categorias_pret)
            self.categorias[new_cat] = []
    
    def elegir_letra(self):
        num_letra = random.randint(0, 25)
        letra = chr(num_letra + ord('A'))
        return letra

    def agregar_palabra(self, categoria, palabra):
        self.categorias[categoria].append(palabra)
        self.palabras[categoria] += palabra + '\n'
        
        
        
    def seleccionar_categoria(self,ronda):
        print("Seleccione una categoría disponible:")
        categorias_disponibles = []
        n = 0
        for i, categoria in enumerate(self.categorias):
            if len(self.categorias[categoria]) == ronda:
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



    def pedir_palabra(self, letra_actual,cat_disp):
        # categoria = self.seleccionar_categoria(ronda)
        print(f"\nIngrese una palabra para la letra {letra_actual} en la categoria {cat_disp}:\n")
        palabra = input()
        while palabra[0].upper() != letra_actual:
            print("ERROR: La palabra ingresada no empieza con la letra " + letra_actual + ". Intentelo nuevamente.\n")
            palabra = input()
        self.agregar_palabra(cat_disp, palabra)

    
    
    def calcular_puntos(self):
        pass
        
        
    
    def resultado_final(self):
        print("Tutti Frutti\n\n")
        print("\nResultado:\n")
        claves = list(self.categorias.keys())
        for cat in claves:  #Encabezado de la tabla
            print("  ",cat,end='    ')
        print("\n")
        i = 0
        for ronda in range(self.rondas):
            print(ronda+1,end=' ')
            for palabra in claves:
                try:
                    print(self.categorias[palabra][i],end="  ")
                except:
                    print("-",end="    ")
            print("\n")
            i += 1



    def jugar(self):
        # Imprimir encabezado
        print("Tutti Frutti\n\n")
        print("Las Categorías para esta partida son:\n")
        for categoria in self.categorias:
            print(f"- {categoria}\n")
            
        # a = str(input("empezamos?"))
        
        for ronda in range(self.rondas):
            
            letra_actual = self.elegir_letra()
            print("La letra de esta ronda es:"+letra_actual+"\n")


            # Solicitar palabras del usuario
            for categoria in self.categorias:
                cat_disp = self.seleccionar_categoria(ronda)
                self.pedir_palabra(letra_actual,cat_disp)
            self.resultado_final()
        print("Fin del juego!")
        

if __name__ == '__main__':
    tf = TuttiFrutti()
    tf.jugar()