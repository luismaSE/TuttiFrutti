import random , threading , time

class TuttiFrutti:
    def __init__(self,q,rounds=2):
        self.rounds = rounds
        self.q = q 
        self.players = {}
        self.table = {}
        self.match = {}
        self.default_cats = [   "animales"   ,"paises/ciudades"   ,
                                "nombres"    ,"deportes/hobbies"  ,
                                "adjetivos"  ,"comidas/bebidas"   ,
                                "marcas"     ,"peliculas/series"  ,
                                "verbos"     ,"colores"           ,  
                                "trabajos"   ,"juegos"
                            ]
        # self.create_tables(num_cats)
        # self.play()

    def add_player(self,nick,player):
        self.players[nick] = player
    
    def add_word(self,round,nick,cat,word):
        self.match[nick][cat][round] = word
        
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
            self.table[new_cat] = ['-' for round in range(self.rounds)]
            for player in list(self.players.keys()):
                self.match[player][new_cat] = ['-' for round in range(self.rounds)]
        print("match",self.match)
                # for round in range(self.rounds):
                #     self.match[player][new_cat].append("-")
                
    

    def play(self):
        th_list = []
        self.categories = list(self.table.keys())
        for round in range(self.rounds):
            self.status = True
            round_letter = self.pick_letter()
            for player in list(self.players.values()):
                thread = threading.Thread(target=player.play_round,args=(round,round_letter,th_list),daemon=True)
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
            
            print(self.match)        

        for nick , player in list(self.players.items()):
            player.send_msg("Fin del juego!\n\nCalculando puntajes...")
        
        return (self.match)
            
        
            
            
            
    def pick_letter(self):
        letter_code = random.randint(0, 25)
        letter = chr(letter_code + ord('A'))
        return letter
    
    
    def show_tables(self,player):
        separator = ''.center(12+(22*len(self.table.keys())),"-")
        player.send_msg("\nTutti Frutti\n\nResultado:\n")
        keys = list(self.table.keys())
        
        
        for nick in list(self.players.keys()):
            player.send_msg(separator+"\n"+nick.center(12+(22*len(self.table.keys())))+"\n"+separator)
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
    
    
    def get_score(self,points):
        score = []
        cats = len(self.get_categories())
        # rounds = int(len(points) / (len(players)*len(cats)))
        for player in range(len(self.players)):
                for round in range(self.rounds):
                    r_score = 0
                    for cat in range(cats):
                        r_score += 10*points[player*self.rounds*cats+cat*self.rounds+round]
                    score.append(r_score)
        return score
    
    def game_over(self,points):
        score = self.get_score(points)
        for  player in list(self.players.values()):
            f_scores = []
            player.send_msg("RESULTADO FINAL:\n")
            self.show_tables(player)
            player.send_msg("PUNTAJES:\n")
            for nick in range(len(self.players)):
                p_score = 0  
                for round in range(self.rounds):
                    r_score = score[nick*self.rounds+round]
                    player.send_msg("Ronda "+str(round)+" = "+str(r_score)+" puntos!\n")
                    p_score += r_score
                f_scores.append(p_score)
                player.send_msg("Puntaje final de "+str(list(self.players.keys())[nick])+" = "+str(p_score)+"\n\n")
                
            max_index = [] 
            max_score = max(f_scores)
            for num in f_scores:
                if num == max_score:
                    max_index.append(f_scores.index(num))
            
            if len(max_index) > 1:
                player.send_msg("Hubó un empate!")
            else:
                player.send_msg("¡El ganador es "+str(list(self.players.keys())[max_index[0]])+"!\n")
            player.send_msg("\n\nGAME OVER")        
                        
            
            
            
            