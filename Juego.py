import os
import random

palabraAdivinada = []
letrasEscritas = []
intentos = 3
palabraSecretaAjustes = "Red"
nombreArchivoGrupos = "Grupos.txt"

def prepararPalabra(original):
    global palabraAdivinada
    original = original.lower()
    palabraAdivinada = []
    for letra in original:
        palabraAdivinada.append({
            "letra": letra,
            "adivinada": False,
        })

def imprimirPalabra():
    for letraCompuesta in palabraAdivinada:
        if letraCompuesta["adivinada"]:
            print(letraCompuesta["letra"], end="")
        else:
            print("-", end="")
    print("")

def imprimirPalabraOriginal():
    for letraCompuesta in palabraAdivinada:
        print(letraCompuesta["letra"], end="")

def descubrirLetra(letraDeUsuario):
    global palabraAdivinada
    global letrasEscritas
    global intentos
    letraDeUsuario = letraDeUsuario.lower()
    if letraDeUsuario in letrasEscritas:
        return
    else:
        letrasEscritas.append(letraDeUsuario)
    if not letraEstaEnPalabra(letraDeUsuario):
        intentos -= 1
    else:
        for letraCompuesta in palabraAdivinada:
            if letraCompuesta["letra"] == letraDeUsuario:
                letraCompuesta["adivinada"] = True

def letraEstaEnPalabra(letra):
    global palabraAdivinada
    for letraCompuesta in palabraAdivinada:
        if letraCompuesta["letra"] == letra:
            return True
    return False

def imprimirAhorcado():
    if intentos == 1:
        print("""
                       ___
                      |   |
                     _O/  |
                      |   |
                     / \  |
                    ______|
        """)
    elif intentos == 2:
        print("""
                       ___
                      |   |
                     _O/  |
                          |
                          |
                    ______|
        """)
    
    elif intentos == 3:
        print("""
                       ___
                      |   |
                      O   |
                          |
                          |
                    ______|
        """)

def dibujarIntentos():
    print("Te quedan " + str(intentos)+ " intentos")

def haGanado():
    global palabraAdivinada
    for letra in palabraAdivinada:
        if not letra["adivinada"]:
            return False
    return True

def obtenerPalabra():
    print('')
    print("¿Con que grupo desea jugar?: \n")
    grupos = obtenerGrupos()
    indice = imprimirGruposYSolicitarIndice(grupos)
    grupo = grupos[indice]
    palabras = obtenerPalabrasDeGrupo(grupo)
    return random.choice(palabras)

def jugar():
    global letrasEscritas
    global intentos
    intentos = 3
    letrasEscritas = []
    palabra = obtenerPalabra()
    prepararPalabra(palabra)
    while True:
        imprimirAhorcado()
        dibujarIntentos()
        imprimirPalabra()
        descubrirLetra(input("Ingresa una letra: "))
        if intentos <= 0:
            print('')
            print("Lo siento. La palabra era: \n")
            imprimirPalabraOriginal()
            return
        if haGanado():
            print('')
            print("Haz ganado, la palabra es:  ", palabra )
            return

def ajustes():
    if input("Ingrese la contraseña: ") != palabraSecretaAjustes:
        print("Contraseña incorrecta")
        return
    menu = """
1. Crear grupo de palabras"""

    grupos = obtenerGrupos()
    eleccion = int(input(menu))
    if eleccion <= 0 or eleccion > 3:
        print("No válido")
        return
    elif eleccion == 1:
        crearGrupoDePalabras(grupos)
   
def imprimirGruposYSolicitarIndice(grupos):
    for i, grupo in enumerate(grupos):
        print(f"{i + 1}. {grupo}\n")
    return int(input("Seleccionar grupo: ")) - 1

def crearGrupoDePalabras(grupos):
    grupo = input("Ingrese el nombre del grupo: ")
    palabras = solicitarPalabrasParaNuevoGrupo()
    escribirPalabrasDeGrupo(palabras, grupo)
    grupos.append(grupo)
    escribirGrupos(grupos)
    print("Grupo creado correctamente")

def escribirGrupos(grupos):
    with open(nombreArchivoGrupos, "w") as archivo:
        for grupo in grupos:
            archivo.write(grupo + "\n")

def escribirPalabrasDeGrupo(palabras, grupo):
    with open(grupo + ".txt", "w") as archivo:
        for palabra in palabras:
            archivo.write(palabra + "\n")

def solicitarPalabrasParaNuevoGrupo():
    palabras = []
    while True:
        palabra = input("Ingrese la palabra o deje el espacio en blanco si quiere terminar: ")
        if palabra == "":
            return palabras
        palabras.append(palabra)
   
def cambiarUnaPalabra(grupo, palabras):
    indice = imprimirPalabrasYSolicitarIndice(palabras)
    palabraCambiada = palabras[indice]
    print("Se cambia la palabra " + palabraCambiada)
    nuevaPalabra = input("Ingresar palabra nueva: ")
    palabras[indice] = nuevaPalabra
    escribirPalabrasDeGrupo(palabras, grupo)
    print("Palabra cambiada correctamente")


def agregarUnaPalabra(grupo, palabras):
    palabra = input("Ingrese la palabra que se agrega: ")
    palabras.append(palabra)
    escribirPalabrasDeGrupo(palabras, grupo)
    print("Palabra agregada correctamente")


def imprimirPalabrasYSolicitarIndice(palabras):
    for i, palabra in enumerate(palabras):
        print(f"{i + 1}. {palabra}")
    return int(input("Seleccione la palabra: ")) - 1


def obtenerGrupos():
    grupos = []
    with open(nombreArchivoGrupos) as archivo:
        for linea in archivo:
            linea = linea.rstrip()
            grupos.append(linea)
    return grupos


def obtenerPalabrasDeGrupo(grupo):
    palabras = []
    with open(grupo + ".txt") as archivo:
        for linea in archivo:
            linea = linea.rstrip()
            palabras.append(linea)
    return palabras


def prepararArchivo():
    if not os.path.isfile(nombreArchivoGrupos):
        with open(nombreArchivoGrupos, "w") as archivo:
            archivo.write("")


def menu_principal():
    menu = """

Bienvenidos al juego del ahorcado

1. Jugar
2. Ajustes

Seleccione una opcion: """
    eleccion = int(input(menu))
    if eleccion == 1:
        jugar()
    elif eleccion == 2:
        ajustes()

def main():
    prepararArchivo()
    while True:
        menu_principal()

main()