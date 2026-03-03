import random

def tirar_dados(cantidad):
    dados = []
    i = 0
    while i < cantidad:
        dados.append(random.randint(1,6))
        i += 1
    return dados

def mostrar_dados(dados):
    i=0
    while i<len(dados):
        print("Posicion:",i,dados[i])
        i+=1
def elegir_dados():
    entrada = input("Ingrese posiciones q quiere volver a tirar sin espacios")

    if entrada == "":
        return []

    resultado = []
    i = 0

    while i < len(entrada):
        resultado.append(int(entrada[i]))
        i += 1

    return resultado
    
    
    
def ordenar_custom(lista):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] > lista[j]:
                lista[i], lista[j] = lista[j], lista[i]
    return lista

def contar_valor(dados, valor):
    contador = 0
    i = 0
    while i < len(dados):
        if dados[i] == valor:
            contador += 1
        i += 1
    return contador

def escalera(dados):
    dados_ord = ordenar_custom(dados)
    
    if dados_ord == [1,2,3,4,5] or dados_ord == [2,3,4,5,6]:
        return True

def poker(dados):
    numero = 1
    while numero <= 6:
        cantidad = contar_valor(dados, numero)
        if cantidad == 4:
            return True
        else:
            numero += 1
        
    
    

def split_custom(texto, separador=" "):
    resultado = []
    palabra = ""
    for char in texto:
        if char == separador:
            if palabra:
                resultado.append(palabra)
                palabra = ""
        else:
            palabra += char
    if palabra:
        resultado.append(palabra)
    return resultado

def es_full(dados):
    tres = False
    dos = False

    numero = 1
    while numero<7:
        cantidad=contar_valor(dados,numero)
        if cantidad==3:
            tres= True
        if cantidad==2:
            dos= True    
        numero+=1
    if tres and dos:
        return True
    else:
        return False
    

def generala(dados):

    numero = 1
    while numero <= 6:
        cantidad = contar_valor(dados, numero)
        if cantidad == 5:
            return True
        numero += 1

    return False



def primer_tirada(dados):
    dados = tirar_dados(5)
    cinco_puntos = False
    if escalera(dados) == True:
        cinco_puntos = True
    if es_full(dados) == True:
        cinco_puntos = True
    if poker(dados) == True:
        cinco_puntos = True
    return cinco_puntos

def generala_real(dados):
    dados = tirar_dados(5)
    treinta_puntos = False
    if generala(dados) == True:
        treinta_puntos = True
    return treinta_puntos
def sumo_numero(dados, numero):
    suma = 0
    i = 0
    while i < len(dados):
        if dados[i] == numero:
            suma += numero
        i += 1
    return suma
import csv
FILE = 'jugadas.csv'
# Escritura de archivo CSV
with open(FILE, 'w', newline='', encoding='utf-8') as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["jugador", "j1", "j2"])
def calcular_puntaje(dados, categoria, primera):
    
    puntos = 0

    if categoria == "E":
        if escalera(dados):
            puntos = 20
            if primera:
                puntos += 5

    elif categoria == "F":
        if es_full(dados):
            puntos = 30
            if primera:
                puntos += 5

    elif categoria == "P":
        if poker(dados):
            puntos = 40
            if primera:
                puntos += 5

    elif categoria == "G":
        if generala(dados):
            puntos = 50
            if primera:
                puntos += 30

    elif categoria in ["1","2","3","4","5","6"]:
        numero = int(categoria)
        puntos = sumo_numero(dados, numero)

    return puntos
def guardar_csv(planilla):
    
    with open(FILE, 'w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)

        escritor.writerow(["jugada", "j1", "j2"])

        for cat in planilla:
            j1 = planilla[cat][0]
            j2 = planilla[cat][1]

            if j1 is None:
                j1 = 0
            if j2 is None:
                j2 = 0

            escritor.writerow([cat, j1, j2])


def turno(jugador, planilla, indice):

    print("\n--- Turno Jugador", jugador, "---")

    dados = tirar_dados(5)

    tirada = 1
    primera = True
    seguir = True

    while tirada <= 3 and seguir:

        print("\nTirada", tirada)
        mostrar_dados(dados)

        if tirada < 3:
            posiciones = elegir_dados()

            if len(posiciones) == 0:
                seguir = False
            else:
                i = 0
                while i < len(posiciones):
                    pos = posiciones[i]
                    if pos >= 0 and pos < 5:
                        dados[pos] = random.randint(1,6)
                    i += 1

                tirada += 1
                primera = False
        else:
            seguir = False

    categorias_disponibles = []

    for cat in planilla:
        if planilla[cat][indice] is None:
            categorias_disponibles.append(cat)

    print("Categorias disponibles:", categorias_disponibles)

    categoria = input("Elija categoria: ").upper()

    while categoria not in categorias_disponibles:
        categoria = input("Categoria invalida. Elija nuevamente: ").upper()

    puntos = calcular_puntaje(dados, categoria, primera)

    planilla[categoria][indice] = puntos

    guardar_csv(planilla)


def main():

    categorias = ["E","F","P","G","1","2","3","4","5","6"]

    planilla = {}

    for cat in categorias:
        planilla[cat] = [None, None]

    guardar_csv(planilla)

    completo = False

    while not completo:

        turno(1, planilla, 0)
        turno(2, planilla, 1)

        completo = True
        i = 0
        while i < len(categorias):
            if planilla[categorias[i]][0] is None or planilla[categorias[i]][1] is None:
                completo = False
            i += 1

    total1 = 0
    total2 = 0

    for cat in planilla:
        if planilla[cat][0] is not None:
            total1 += planilla[cat][0]
        if planilla[cat][1] is not None:
            total2 += planilla[cat][1]

    print("\n===== RESULTADO FINAL =====")
    print("Jugador 1:", total1)
    print("Jugador 2:", total2)

    if total1 > total2:
        print("Gana Jugador 1")
    elif total2 > total1:
        print("Gana Jugador 2")
    else:
        print("Empate")


main()



