import requests
import json
import ast
from bardapi import Bard, SESSION_HEADERS

def api_query(dict):
    
    resp = """#
{
  "Luisma": {
    "aves": {
      "zorro": 0,
      "golondrina": 1,
      "ardilla": 1
    },
    "colores": {
      "zian": 0,
      "gris": 1,
      "amarillo": 1
    }
  },
  "Juan": {
    "aves": {
      "ztucan": 0,
      "gato": 0,
      "aguila": 1
    },
    "colores": {
      "zrojo": 0,
      "gris": 1,
      "anaranjado": 1
    }
  }
}
#

He utilizado el siguiente criterio para clasificar las palabras:

* **Sustantivos:** palabras que designan personas, animales, cosas, lugares o ideas.
* **Adjetivos:** palabras que acompañan a un sustantivo para expresar una cualidad o condición.
* **Verbos:** palabras que expresan una acción, un estado o un proceso.
* **Adverbios:** palabras que modifican a un verbo, un adjetivo o otro adverbio.

En el caso de los errores ortográficos, he considerado que la palabra no pertenece a la categoría si el error es lo suficientemente grave como para cambiar su significado. Por ejemplo, la palabra "zian" no es un sustantivo, sino un error ortográfico de la palabra "cian".

Espero que esta respuesta sea correcta."""

    
    # session = requests.Session()
    # token = "aAhrFPgLwZoeTEPQQxVkVl3upOMYjJFDoQ9lA-bkAPDA_VXjO79b9TaJDZJugQ66Z0SLLw."
    # session.cookies.set("__Secure-1PSID", token)
    # session.cookies.set( "__Secure-1PSIDCC", "APoG2W9nKPJN7wm-fxy3UFu0B0oIYXlI35w_3ePffwpbn1HwR7b99JpEW6sxWmQwAbXfBxYf")
    # session.cookies.set("__Secure-1PSIDTS", "sidts-CjIBSAxbGX4eK6sbC6yAsCS1wR0IPcIEd3rrDY3_kUXelVI0her43HnIXhV3LqJOB2Y9thAA")
    # session.headers = SESSION_HEADERS

    # bard = Bard(token, session=session,conversation_id="c_1f04f704a788e6e4", timeout=30)

    # texto = dict+"""
    # Toma este diccionario y agrega un 1 o un 0 si la palabra pertenece a la categoría, los errores ortograficos no se permiten.
    # SOLO RESPONDE EL DICCIONARIO MODIFICADO EN FORMATO JSON, NADA DE CODIGO, NADA DE EXPLICACIONES
    
    # Responder siguiendo este formato:
    
    # Signo #
    # diccionario json
    # Signo #.

    # Solo eso, ni una sola palabra más
    
    # EJEMPLO:
    # {'jugador1': {'colores': ['Gris', 'turquesa', 'hugo'], 'animales': ['gato', 'tomate', 'helefante']}, 'jugador2': {'colores': ['gris','-','halamo'], 'animales': ['ganzo','tiburon', '-']}}
    
    # RESPUESTA ESPERADA DEL EJEMPLO:
    # {"jugador1": {"colores": {"Gris":1, "turquesa":1, "hugo":0}, "animales": {"gato":1, "tomate":0, "helefante":0}}, "jugador2": {"colores": {"gris":1,"-":0,"halamo":0}, "animales": {"ganzo":1,"tiburon":1, "-":0}}}

    # """
    # resp = bard.get_answer(texto)["content"]
    # print(resp)
    
    dict = json.loads(resp.split('#')[1])
    print(dict)
    print(type(dict))
    return dict
    

if __name__ == "__main__":
    dic = "{'Luisma': {'aves': ['zorro', 'golondrina', 'ardilla'], 'colores': ['zian', 'gris', 'amarillo']}, 'Juan': {'aves': ['ztucan', 'gato', 'aguila'], 'colores': ['zrojo', 'gris', 'anaranjado']}}"
    api_query(dic)















# from bardapi import ChatBard

# chat.start(prompt="Enter your message: ")
# chat.start()












# import requests
# from bardapi import Bard, SESSION_HEADERS

# session = requests.Session()
# session.cookies.set("__Secure-1PSID", "bard __Secure-1PSID token")
# session.cookies.set( "__Secure-1PSIDCC", "bard __Secure-1PSIDCC token")
# session.cookies.set("__Secure-1PSIDTS", "bard __Secure-1PSIDTS token")
# session.headers = SESSION_HEADERS

# bard = Bard(session=session)
# bard.get_answer("")

















# from bardapi import Bard
# import os
# import requests
#          aAhrFIwxk1WT8oHtfJkvuSFE3vDyNV_fP_fsRh1JDd0j9z6ZyFeSUGIQwt4bUzaV9-s7SQ.
# token = 'aAhrFIwxk1WT8oHtfJkvuSFE3vDyNV_fP_fsRh1JDd0j9z6ZyFeSUGIQwt4bUzaV9-s7SQ.'
# os.environ['_BARD_API_KEY'] = token
# # token='aAjdHJ3eKwntcEzs3GAEDBoqm2dk1ri43vxrw_DllyA-G8zPRVctWtAsc7EC_WC2uiN6lw.'

# session = requests.Session()
# session.headers = {
#             "Host": "bard.google.com",
#             "X-Same-Domain": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
#             "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
#             "Origin": "https://bard.google.com",
#             "Referer": "https://bard.google.com/",
#         }
# session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY")) 
# # session.cookies.set("__Secure-1PSID", token) 

# bard = Bard(token=token, session=session, timeout=30)
# print(bard.get_answer("'Luisma': {'paises': ['Lisboa'], 'comida': ['lasagna']}, 'wey': {'paises': ['lomo'], 'comida': ['lentejas']} toma este diccionario y decime que palabras no pertenecen a su categoria")['content'])
# print(bard.get_answer("cual fue mi ultima pregunta?")["content"])







# session.cookies.set("__Secure-1PSID", "aAjdHJ3eKwntcEzs3GAEDBoqm2dk1ri43vxrw_DllyA-G8zPRVctWtAsc7EC_WC2uiN6lw.")
# session.cookies.set( "__Secure-1PSIDCC", "APoG2W_5VhvZAHu2aeHL6cXamiaa36V7m6k-gqT8TP0MgtfkQGdTRB7e9QsqPHX_Rvvztj__Ibg")
# session.cookies.set("__Secure-1PSIDTS", "sidts-CjIBSAxbGWvHxSbbqNjjlqOSb8zoNNq2XyljNMyZUimaa9EwL3bjpenmAvQaRPHHaCNRERAA")
