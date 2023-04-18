import random , threading , time

class TuttiFrutti:
    def __init__(self,q,rounds=2):
        self.rounds = rounds
        self.q = q 
        self.players = {}
        self.table = {}
        self.match = {}
        self.default_cats = [   "animales" ,"paises"  ,"Nombres"  ,"peliculas",
                                "series"   ,"ropa"    ,"deportes" ,"peces"    ,
                                "mamiferos","reptiles","aves"     ,"adjetivos",
                                "verbos"   ,"colores" ,"comida"   ,"bebida"   ]
        
        # self.create_tables(num_cats)
        # self.play()

    def add_player(self,nick,player):
        self.players[nick] = player
    
    def add_word(self,nick,cat,word):
        self.match[nick][cat].append(word)
        
    def get_categories(self):
        return list(self.table.keys())
    
    def get_status(self):
        return self.status
    
    def create_tables(self,num_cats):
        new_cat = ''
        for player in list(self.players.keys()):
            self.match[player] = {}
        for col in range(num_cats):
            while new_cat == '' or new_cat in self.table.keys():
                new_cat = random.choice(self.default_cats)
            self.table[new_cat] = []
            for player in list(self.players.keys()):
                self.match[player][new_cat] = []
    

    def play(self):
        th_list = []
        categories = list(self.table.keys())
        for round in range(self.rounds):
            self.status = True
            round_letter = self.pick_letter()
            for player in list(self.players.values()):
                thread = threading.Thread(target=player.play_round,args=(round_letter,th_list),daemon=True)
                th_list.append(thread)
                thread.start()
                
            # print("Espero a que alguien termine")
            end = self.q.get()
            end_warning = end[0]+' gritó '+end[1][1:-2]
            self.status = False
            print("Recibi:",end_warning)
            
            
            for nick , player in list(self.players.items()):
                if nick != end[0]:
                    # print("le aviso a ",nick)
                    player.send_msg(end_warning)
            for th in th_list:
                th.join()
            for nick , player in list(self.players.items()):
                self.show_tables(player)
                player.send_msg("Preparate, la proxima ronda esta por empezar...")
            
            time.sleep(3)

        # ("Fin del juego!")
            
            
    def pick_letter(self):
        letter_code = random.randint(0, 25)
        letter = chr(letter_code + ord('A'))
        return letter
    
    
    def show_tables(self,player):
        separator = ''.center(13+(23*len(self.table.keys())),"-")
        player.send_msg("\nTutti Frutti\n\nResultado:\n")
        keys = list(self.table.keys())
        
        
        for nick in list(self.players.keys()):
            player.send_msg(separator+"\n"+nick.center(13+(23*len(self.table.keys())))+"\n"+separator)
            header = ("|"+"Ronda".center(10)+"|")
            
            for key in keys:
                header += ("|"+ key.center(20)+"|")
            player.send_msg(header+"\n")
                            
            
            i = 0
            for round in range(self.rounds):
                row = ''
                row += ("|"+str(round+1).center(10)+"|")
                for word in keys:            
                    try:
                        row += ("|"+self.match[nick][word][i].center(20)+"|")
                    except:
                        row += ("|"+"-".center(20)+"|")
                i += 1
                player.send_msg(row+"\n")
            player.send_msg(separator+"\n\n")
    
    
    def points(self):
        pass