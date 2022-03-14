# coding: utf-8

# define dictionaries containing verb endings
class Endings:
    def __init__(self): 
        self.present_indicative = {"name": "present_indicative",
                                   "ar": ["o", "as", "a", "amos", "áis", "an"],
                                   "er": ["o", "es", "e", "emos", "éis", "en"],
                                   "ir": ["o", "es", "e", "imos", "ís", "en"]}
        self.preterite_indicative = {"name": "preterite_indicative",
                                     "ar": ["é", "aste", "ó", "amos", "asteis", "aron"],
                                     "er": ["í", "iste", "ió", "imos", "isteis", "ieron"],
                                     "ir": ["í", "iste", "ió", "imos", "isteis", "ieron"]} 
        self.future_indicative = {"name": "future_indicative",
                                  "ar": ["aré", "arás", "á", "emos", "aréis", "arán"],
                                  "er": ["eré", "erás", "á", "emos", "eréis", "erán"],
                                  "ir": ["iré", "irás", "á", "emos", "iréis", "irán"]}

endings = Endings()
#print(endings.present_indicative)

list_of_irreg_verbs = ["ser",
                        "haber",
                        "estar",
                        "tener",
                        "hacer",
                        "poder",
                        "decir",
                        "ir",
                        "ver",
                        "dar",
                        "saber",
                        "querer",
                        "llegar",
                        "poner",
                        "parecer",
                        "creer",
                        "seguir",
                        "encontrar",
                        "venir",
                        "pensar",
                        "salir",
                        "volver",
                        "conocer",
                        "sentir",
                        "contar",
                        "emezar",
                        "buscar",
                        "escribir",
                        "perder",
                        "producir",
                        "entender",
                        "pedir",
                        "recordar",
                        "aparecer",
                        "conseguir",
                        "comenzar",
                        "servir",
                        "sacar",
                        "mantener",
                        "leer",
                        "caer",
                        "abrir",
                        "convertir",
                        "traer",
                        "morir",
                        "realizar",
                        "suponer",
                        "explicar",
                        "tocar",
                        "reconocer",
                        "alcanzar",
                        "nacer",
                        "dirigir",
                        "utilizar",
                        "pagar",
                        "jugar",
                        "ofrecer",
                        "descubrir",
                        "repetir",
                        "valer",
                        "mostrar",
                        "mover",
                        "continuar",
                        "referir",
                        "acercar",
                        "dedicar",
                        "cerrar",
                        "obtener",
                        "indicar",
                        "soler",
                        "detener",
                        "elegir",
                        "proponer",
                        "demostrar",
                        "significar",
                        "reunir",
                        "construir",
                        "desaparecer",
                        "andar",
                        "preferir",
                        "crecer",
                        "surgir",
                        "entregar",
                        "colocar",
                        "establecer",
                        "actuar",
                        "acordar",
                        "romper",
                        "adquirir",
                        "lanzar",
                        "negar",
                        "avanzar",
                        "resolver",
                        "costar",
                        "exigir",
                        "recoger",
                        "imponer",
                        "obligar",
                        "aplicar"]

def conjugate(verb):
    if verb in list_of_irreg_verbs:
        return("sorry, that's irregular and I can't handle irregular verbs yet!")
    
    else:
        stem = verb[:-2]
        
        conjugated_verbs = []
        
        conjugated_present_indicative = [stem + x for x in endings.present_indicative[verb[-2:]]]
        conjugated_preterite_indicative = [stem + x for x in endings.preterite_indicative[verb[-2:]]]
        conjugated_future_indicative = [stem + x for x in endings.future_indicative[verb[-2:]]]
        
        return(conjugated_present_indicative, 
               conjugated_preterite_indicative, 
               conjugated_future_indicative)
