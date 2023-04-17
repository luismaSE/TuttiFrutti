import random , pickle , threading , queue , time

class TuttiFrutti:
    def __init__(self,players={'Luisma':111,'Sofi':222},rounds=2,num_cats=2):
        self.players = players
        self.rounds = rounds
        self.table = {}
        self.match = {}
        self.default_cats = [   "animales" ,"paises"  ,"Nombres"  ,"peliculas",
                                "series"   ,"ropa"    ,"deportes" ,"peces"    ,
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
            

    def start_match(self):
        for nick , client in list(self.players.items()):
            client.sendall(pickle.dumps(f"\nHola {nick}!\nVamos a jugar al Tutti Frutti!\n\nLas Categorías para esta partida son:\n"))                                    
            cats = ''
            for cat in self.table:
                cats += f"- {cat}\n"
            client.sendall(pickle.dumps(cats))

    def play(self):
        th_list = []
        th_q = queue.Queue()
        
        for round in range(self.rounds):
            self.status = True
            round_letter = self.pick_letter()
            for nick , client in list(self.players.items()):
                thread = threading.Thread(target=self.play_round,args=(nick,client,round_letter,th_list,th_q),daemon=True)
                th_list.append(thread)
                thread.start()
                
            print("Espero a que alguien termine")
            end = th_q.get()
            self.status = False
            print("Recibi:",end)
            
            
            for nick , client in list(self.players.items()):
                if nick != end[0]:
                    print("le aviso a ",nick)
                    client.sendall(pickle.dumps(end))
            for th in th_list:
                th.join()
            for nick , client in list(self.players.items()):
                self.show_tables(client)
                client.sendall(pickle.dumps("Preparadate, la proxima ronda esta por empezar..."))
            
            time.sleep(3)

            
            
        
        # thread.join()
            # for nick , client in list(self.players.items()):
                
                 
        client.sendall(pickle.dumps("Fin del juego!"))
        
    def pick_letter(self):
        letter_code = random.randint(0, 25)
        letter = chr(letter_code + ord('A'))
        return letter
        
        
    def play_round(self,nick,client,round_letter,th_list,th_q):
        client.sendall(pickle.dumps("----------------------------------------------------------------------"))    
        client.sendall(pickle.dumps("\nLa letra de esta ronda es:"+round_letter+"\n"))
        avail_cats = list(self.table.keys())
        for cat in self.table:
            if self.status:
                print('status es 1 - juego')
                mi_cat = self.pick_cat(client,avail_cats)
                avail_cats.pop(avail_cats.index(mi_cat))
            if self.status:                
                word = self.get_word(client,round_letter,mi_cat)
                print(f"agrego la palabra {word}, a la categoria {mi_cat}, en la tabla de {nick}")
                self.add_word(nick,mi_cat,word)
                print(self.match[nick])
            else:
                print(f"status es 0. {nick}, alguien ya terminó")
                break
        if self.status:
            client.sendall(pickle.dumps("Tutti Frutti, Nadie más escribe!"))
            th_q.put([nick,"Tutti Frutti, Nadie más escribe!*"])
            th_list.remove(threading.current_thread())
        
        
        # TO DO: El hilo debe revisar si alguien ya terminó y segun donde se encuentre el cliente en ese momento, dejarlo ingresar la palabra o cortarlo ahi
        
        # self.show_tables(client)     #Esto lo va a tener q hacer el proceso de la partida para cada cliente (para que todos vean la misma tabla, al mismo tiempo)
        
    
    def pick_cat(self,client,avail_cats):
        client.sendall(pickle.dumps("Categorías disponibles:"))
        n = 0 ; cats = ''
        for cat in avail_cats:
            n += 1
            cats += (f"{n}. {cat}\n")
        client.sendall(pickle.dumps(cats))        
        if len(avail_cats) == 1:
            return avail_cats[0]
        # client.sendall(pickle.dumps("\n"))    
        client.sendall(pickle.dumps("# Seleccione una opción:"))
        cat_num = int(pickle.loads(b'' + client.recv(4096)))
        while cat_num not in range(1, len(avail_cats) + 1):
            client.sendall(pickle.dumps("# Opción inválida. Seleccione una categoría disponible:"))
            cat_num = int(pickle.loads(b'' + client.recv(4096)))
        return avail_cats[cat_num-1]



    def get_word(self,client,round_letter,mi_cat):
        client.sendall(pickle.dumps((f"# Ingrese una palabra para la letra {round_letter} en la categoria {mi_cat}:\n")))
        word = pickle.loads(b'' + client.recv(4096))
        while word[0].upper() != round_letter:
            client.sendall(pickle.dumps("# ERROR: La palabra ingresada no empieza con la letra " + round_letter + ". Intentelo nuevamente.\n"))
            word = pickle.loads(b'' + client.recv(4096))
        return word


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