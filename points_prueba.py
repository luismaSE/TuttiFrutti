def calcular_puntajes(players,cats,words,points):
    puntajes = []
    rounds = int(len(points) / (len(players)*len(cats)))
    for player in range(len(players)):
            for round in range(rounds):
                r_point = 0
                for cat in range(len(cats)):
                    print(words[player*rounds*len(cats)+cat*rounds+round])
                    r_point += 15*points[player*rounds*len(cats)+cat*rounds+round]
                print('fin de ronda')
                puntajes.append(r_point)
    return puntajes






if __name__ == '__main__':
    
    players = ['Luisma', 'Juan']
    cats = ['aves', 'colores']
    words = ['zorro', 'golondrina', 'ardilla',       'zian', 'gris', 'amarillo',          
                    'ZORRO', 'gato', 'aguila',       'zrojo', 'gris', 'anaranjado']
    points = [  0,   2,   0,          0,   1,   2,             
                0,   0,   2,          0,   1,   2]

    calcular_puntajes(players,cats,words,points)
    # puntajes_rondas, puntaje_final = calcular_puntajes(entrada)
    # print("Puntajes por ronda:", puntajes_rondas)
    # print("Puntaje final:", puntaje_final)
