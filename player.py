import pickle , threading , select


class Player:

    def __init__(self,q,nick,client):
        self.q = q
        self.nick = nick
        self.client = client
        
    def join_match(self,tf):
        self.tf = tf
        
    def start_match(self):
        self.send_msg(f"\nHola {self.nick}!\nVamos a jugar al Tutti Frutti!\n\nLas Categorías para esta partida son:\n")
        cats = ''
        for cat in self.tf.get_categories():
            cats += f"- {cat}\n"
        self.send_msg(cats)
    
    # def send_msg(self,msg):
    #     self.client.sendall(pickle.dumps(msg))
    

    # def recv_msg(self):
    #     data = b'' ; packet = b''
    #     while (len(packet) == 1024 or packet == b''):
    #         packet = self.client.recv(1024)
    #         if packet == b'':
    #             return None
    #         data += packet
    #     return pickle.loads(data)
    
    def send_pickle_msg(self,msg):
        self.client.sendall(pickle.dumps(msg))

    def send_msg(self,msg):
        self.client.sendall(msg.encode())

    def recv_pickle_msg(self):
        return pickle.loads(self.client.recv(1024))

    def recv_msg(self):
        return self.client.recv(1024).decode()
    
    
    def play_round(self,round_letter,th_list):
        self.send_msg("\nLa letra de esta ronda es:"+round_letter+"\n")
        avail_cats = self.tf.get_categories()
        for cat in self.tf.get_categories():
            
            if self.tf.get_status():
                # print('status es 1 - juego')
                mi_cat = self.pick_cat(avail_cats)
                avail_cats.pop(avail_cats.index(mi_cat))
                
            if self.tf.get_status():                
                word = self.get_word(round_letter,mi_cat)
                # print(f"agrego la palabra {word}, a la categoria {mi_cat}, en la tabla de {self.nick}")
                self.add_word(mi_cat,word)
            
            else:
                # print(f"status es 0. {self.nick}, alguien ya terminó")
                break
            
        if self.tf.get_status():
            self.send_msg("Tutti Frutti, Nadie más escribe!")
            self.q.put([self.nick,"*¡Tutti Frutti, Nadie más escribe!*"])
            th_list.remove(threading.current_thread())
        
        
            
    def pick_cat(self,avail_cats):
        self.send_msg("Categorías disponibles:")
        n = 0 ; cats = ''
        for cat in avail_cats:
            n += 1
            cats += (f"{n}. {cat}\n")
        self.send_msg(cats)
        if len(avail_cats) == 1:
            return avail_cats[0]
        self.send_msg("# Ingrese la opción que quiere completar:")
        cat_num = int(self.recv_msg())
        while cat_num not in range(1, len(avail_cats) + 1):
            self.send_msg("# Opción inválida. Ingrese una categoría disponible: ")
            cat_num = int(self.recv_msg())
        return avail_cats[cat_num-1]



    def get_word(self,round_letter,mi_cat):
        self.send_msg(f"# Ingrese una palabra para la letra {round_letter} en la categoria {mi_cat}: ")
        word = self.recv_msg()
        while word[0].upper() != round_letter:
            self.send_msg("# ERROR: La palabra Ingresada no empieza con la letra " + round_letter + ". Intentelo nuevamente: ")
            word = self.recv_msg()
        return word



    def add_word(self,cat,word):
        self.tf.add_word(self.nick,cat,word)