import random , asyncio ,  concurrent.futures , os

class TuttiFrutti:
    def __init__(self,players={'Luisma':111,'Sofi':222},rounds=2,num_cats=3):
        self.players = players
        # self.size = len(self.players)
        self.rounds = rounds
        self.match = {}
        self.table = {}
        self.default_cats = ["animales" ,"paises"  ,"Nombres"  ,"peliculas",
                                "series"   ,"ropa"    ,"deportes" ,"peces"    ,
                                "mamiferos","reptiles","aves"     ,"adjetivos",
                                "verbos"   ,"colores" ,"comida"   ,"bebida"   ]
        
        self.crear_tablas(num_cats)
        
    
    def create_tables(self,num_cats):
        for player in list(self.players.keys()):
            self.match[player] = {}
        new_cat = ''
        for col in range(num_cats):
            while new_cat == '' or new_cat in self.table.keys():
                new_cat = random.choice(self.default_cats)
            self.table[new_cat] = []
            for player in list(self.players.keys()):
                self.match[player][new_cat] = []
    
    
    
    def pick_letter(self):
        letter_code = random.randint(0, 25)
        letter = chr(letter_code + ord('A'))
        return letter

    def add_word(self,player, cat, word):
        self.match[player][cat].append(word)
        
        
        
    def pick_cat(self,player,round):
        print("Seleccione una categoría disponible:")
        empty_cats = []
        n = 0
        for cat in list(self.table.keys()):
            if len(self.match[player][cat]) == round:
                n += 1
                print(f"{n}. {cat}")
                empty_cats.append(cat)
                
        if len(empty_cats) == 1:
            return empty_cats[0]
        
        cat_num = int(input())
        while cat_num not in range(1, len(empty_cats) + 1):
            print("Opción inválida. Seleccione una categoría disponible:")
            cat_num = int(input())
        return empty_cats[cat_num-1]



    def get_word(self,player,round_letter,avail_cat):
        print(f"\nIngrese una palabra para la letra {round_letter} en la categoria {avail_cat}:\n")
        word = input()
        while word[0].upper() != round_letter:
            print("ERROR: La palabra ingresada no empieza con la letra " + round_letter + ". Intentelo nuevamente.\n")
            word = input()
        self.add_word(player,avail_cat, word)

    
    
    def points(self):
        pass
        
        
    
    def show_tables(self):
        row = ''.center(13+(23*len(self.table.keys())),"-")
        print("Tutti Frutti\n\n")
        print("\nResultado:\n")
        keys = list(self.table.keys())
        for player in list(self.match.keys()):
            print(row)
            print(player.center(13+(23*len(self.table.keys()))))
            print(row)
            print("|","Ronda".center(10),end="|")
            for cat in keys:  #Encabezado de la tabla
                print("|",cat.center(20),end="|")
            print("\n")
            i = 0
            for round in range(self.rounds):
                print("|",str(round+1).center(10),end="|")
                for word in keys:
                    try:
                        print("|",self.match[player][word][i].center(20),end="|")
                    except:
                        print("|","-".center(20),end="|")
                print("\n")
                i += 1
            print(row,"\n\n")



    def play(self,player):
        print("Tutti Frutti\n\n")
        print("Las Categorías para esta partida son:\n")
        for cat in self.table:
            print(f"- {cat}\n")
            
        # a = str(input("empezamos?"))
        
        for round in range(self.rounds):
            round_letter = self.pick_letter()
            print("La letra de esta ronda es:"+round_letter+"\n")
            
            for cat in self.table:
                print(f"{player} te toca!")
                    # Solicitar palabras del usuario
                avail_cat = self.pick_cat(player,round)
                self.get_word(player,round_letter,avail_cat)
                    # print(self.table)
                    # print(self.match)
            self.show_tables()
        print("Fin del juego!")
        
        
    async def main(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for player in list(self.players.keys()):
                future = loop.run_in_executor(executor,self.play(player))
                result = await future
                print(result)

if __name__ == '__main__':
    print(f"PID PRINCIPAL: {os.getpid()}")
    tf = TuttiFrutti()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tf.main())