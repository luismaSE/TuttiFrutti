import random , asyncio ,  signal , os , multiprocessing as mp , pickle

class TuttiFrutti:
    def __init__(self,players={'Luisma':111,'Sofi':222},rounds=2,num_cats=3):
        self.players = players
        self.rounds = rounds
        self.table = {}                                                                                 # Tabla vacia de la partida, el programa itera sobre esta en vez de la de un jugador
        self.match = {}
        self.default_cats = [   "animales" ,"paises"  ,"Nombres"  ,"peliculas",
                                "series"   ,"ropa"    ,"deportes" ,"peces"    ,                         # Categorias disponibles para armar la partida
                                "mamiferos","reptiles","aves"     ,"adjetivos",
                                "verbos"   ,"colores" ,"comida"   ,"bebida"   ]
        self.create_tables(num_cats)
        self.start_match()
        self.play()

    
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
        # print(f"MATCH>>>{self.match}")
            

    def start_match(self):
        for nick , client in list(self.players.items()):
            # print(f"PID del proceso del jugador({nick}): {os.getpid()}")
            client.sendall(pickle.dumps("Tutti Frutti\n\nLas Categorías para esta partida son:\n\n"))                                    
            cats = ''
            for cat in self.table:
                cats += f"- {cat}\n"
            client.sendall(pickle.dumps(cats))
            

    def play(self):
        q = mp.Queue()        
        for round in range(self.rounds):
            round_letter = self.pick_letter()
            processes = []
            for nick , client in list(self.players.items()):
                proc = mp.Process(target=self.play_round,args=(q,nick,client,round_letter,round))
                proc.start()
                processes.append(proc)
            while True:
                player , cat , msg = q.get()
                print(f"RECIBI>>>>{player},{cat},{msg}")
                if cat == None:
                    break
                self.add_word(player,cat,msg)
                print (f"Tablas>>>>{self.match}")
                
            for process in processes:
                if process.is_alive():
                    process.terminate()
                    
            self.show_tables(client)                                                                                #Solamente al final de cada ronda podran ver las tablas de los demas jugadores
        client.sendall(pickle.dumps("Fin del juego!"))
        
    def pick_letter(self):
        letter_code = random.randint(0, 25)
        letter = chr(letter_code + ord('A'))
        return letter
        
        
    def play_round(self,q,nick,client,round_letter,round):    
            client.sendall(pickle.dumps("La letra de esta ronda es:"+round_letter+"\n\n"))
            avail_cats = list(self.table.keys())
            # print(f"DISPONIBLES>>>>{avail_cats}")
            for cat in self.table:
                # client.sendall(pickle.dumps(f"{nick} te toca!\n"))
                mi_cat = self.pick_cat(client,avail_cats)
                avail_cats.pop(avail_cats.index(mi_cat))                
                word = self.get_word(client,nick,round_letter,mi_cat)
                q.put([nick,mi_cat,word])    
            q.put([nick,None,"Tutti Frutti, nadie más escribe!"])
    
    def pick_cat(self,client,avail_cats):
        # empty_cats = []
        client.sendall(pickle.dumps("Categorías disponibles:"))
        n = 0 ; cats = ''
        # print(f'{self.match}')
        for cat in avail_cats:
            # if len(self.match[player][cat]) == round:
            n += 1
            cats += (f"{n}. {cat}\n")
            # empty_cats.append(cat)
        client.sendall(pickle.dumps(cats))        
        if len(avail_cats) == 1:
            return avail_cats[0]
        client.sendall(pickle.dumps("# Seleccione una opción:"))
        cat_num = int(pickle.loads(b'' + client.recv(4096)))
        while cat_num not in range(1, len(avail_cats) + 1):
            client.sendall(pickle.dumps("# Opción inválida. Seleccione una categoría disponible:"))
            cat_num = int(pickle.loads(b'' + client.recv(4096)))
        return avail_cats[cat_num-1]



    def get_word(self,client,player,round_letter,mi_cat):
        client.sendall(pickle.dumps((f"# Ingrese una palabra para la letra {round_letter} en la categoria {mi_cat}:\n")))
        word = pickle.loads(b'' + client.recv(4096))
        while word[0].upper() != round_letter:
            client.sendall(pickle.dumps("# ERROR: La palabra ingresada no empieza con la letra " + round_letter + ". Intentelo nuevamente.\n"))
            word = pickle.loads(b'' + client.recv(4096))
        return word
        # self.add_word(player,mi_cat, word)


    def add_word(self,player, cat, word):
        self.match[player][cat].append(word)
        
    
    def show_tables(self,client):
        separator = ''.center(13+(23*len(self.table.keys())),"-")
        client.sendall(pickle.dumps("Tutti Frutti\n\n\nResultado:\n"))
        keys = list(self.table.keys())
        
        
        for player in list(self.match.keys()):
            client.sendall(pickle.dumps((separator+"\n"+player.center(13+(23*len(self.table.keys())))+"\n"+separator)))
            header = ("|"+"Ronda".center(10)+"|")
            
            for key in keys:
                header += ("|"+ key.center(20)+"|")
            client.sendall(pickle.dumps(header+"\n"))
                            
            
            i = 0
            for round in range(self.rounds):
                row = ''
                row += ("|"+str(round+1).center(10)+"|")
                for word in keys:            
                    try:
                        row += ("|"+self.match[player][word][i].center(20)+"|")
                    except:
                        row += ("|"+"-".center(20)+"|")
                i += 1
                client.sendall(pickle.dumps(row+"\n"))
            client.sendall(pickle.dumps(separator+"\n\n"))
    
    
    def points(self):
        pass
        
        






    # def play(self,player,client):                                                                                 # Aca corre el proceso/hilo de cada jugador 
    #     print(f"PID del proceso del jugador({player}): {os.getpid()}")
    #     client.sendall(pickle.dumps("Tutti Frutti\n\nLas Categorías para esta partida son:\n\n"))                                                                           # Cada usuario debe ver solo su tabla a lo largo de toda la ronda
    #     cats = ''
    #     for cat in self.table:
    #         cats += f"- {cat}\n"
    #     client.sendall(pickle.dumps(cats))
            
        # a = str(input("empezamos?"))
        
        # for round in range(self.rounds):
        #     round_letter = self.pick_letter()
        #     client.sendall(pickle.dumps("La letra de esta ronda es:"+round_letter+"\n\n"))
            
        #     for cat in self.table:
        #         client.sendall(pickle.dumps(f"{player} te toca!\n"))
        #         mi_cat = self.pick_cat(client,player,round)                
                
        #         self.get_word(client,player,round_letter,mi_cat)
                    # print(self.table)
                    # print(self.match)
                    
        
        
    
      
        
    # def main(self):
    #     print(f"PID de la partida: {os.getpid()}")
    #     for nick , client  in list(self.players.items()):  
    #         print(f"lanzo un proceso para ({nick})")  
    #         mp.Process(target=self.play,args=(nick,client)).start()
            
            
            
    # async def main(self):                                                                                     # Tiene que lanzarse un hilo o proceso para cada usuario
    #     with concurrent.futures.ThreadPoolExecutor() as executor:                                             # Para que cada uno corra la funcion play() por su cuenta
    #         for player in list(self.players.keys()):
    #             future = loop.run_in_executor(executor,self.play(player))
    #             result = await future
    #             print(result)

# if __name__ == '__main__':
#     print(f"PID PRINCIPAL: {os.getpid()}")
#     tf = TuttiFrutti()
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(tf.main())