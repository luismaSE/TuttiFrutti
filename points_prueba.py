def calcular_puntajes(diccionario):
    puntajes_rondas = []
    
    for ronda, categorias_jugadores in enumerate(diccionario.values()):
        puntaje_ronda = {}
        
        for jugador, categorias in categorias_jugadores.items():
            for categoria, respuestas in categorias.items():
                if jugador not in puntaje_ronda:
                    puntaje_ronda[jugador] = 0
                
                puntaje_categoria = 0
                respuesta_contador = {}
                
                for respuesta, valor in respuestas.items():
                    if valor == 1:
                        if respuesta in respuesta_contador:
                            if respuesta_contador[respuesta] == 1:
                                puntaje_categoria += 5
                            elif respuesta_contador[respuesta] > 1:
                                puntaje_categoria += 0
                        else:
                            respuesta_contador[respuesta] = 1
                            puntaje_categoria += 10
                    else:
                        respuesta_contador[respuesta] = 0
                        
                puntaje_ronda[jugador] += puntaje_categoria
        
        puntajes_rondas.append(puntaje_ronda)
    
    puntaje_final = {}
    for ronda_puntajes in puntajes_rondas:
        for jugador, puntaje in ronda_puntajes.items():
            if jugador not in puntaje_final:
                puntaje_final[jugador] = 0
            puntaje_final[jugador] += puntaje
    
    return puntajes_rondas, puntaje_final

# Diccionario de ejemplo
entrada = {
    'Luisma': {
        'aves': {'zorro': 0, 'golondrina': 1, 'ardilla': 1},
        'colores': {'zian': 0, 'gris': 1, 'amarillo': 1}
    },
    'Juan': {
        'aves': {'ztucan': 0, 'gato': 0, 'aguila': 1},
        'colores': {'zrojo': 0, 'gris': 1, 'anaranjado': 1}
    }
}

puntajes_rondas, puntaje_final = calcular_puntajes(entrada)
print("Puntajes por ronda:", puntajes_rondas)
print("Puntaje final:", puntaje_final)
