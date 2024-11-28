import board
import movimiento as mv
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_tablero(tablero):
    limpiar_pantalla()
    print('    ', end='')
    for i in range(len(tablero[0])):
        print(f'{i + 1} ', end='')
    print()
    for i, fila in enumerate(tablero):
        print(f'{i + 1} | ', end='')
        for columna in fila:
            print(columna, end=' ')
        print(f'| {i + 1}')
    print('    ', end='')
    for i in range(len(tablero[0])):
        print(f'{i + 1} ', end='')
    print()

def buscar_robot(tablero):
    for i, fila in enumerate(tablero):
        for j, columna in enumerate(fila):
            if columna == board.ROBOT:
                return i, j
    return -1, -1

def mover_robot(tablero, direccion):
    fila, columna = buscar_robot(tablero)
    fila_obj, columna_obj = fila, columna

    if direccion == mv.ARRIBA:
        fila_obj -= 1
    elif direccion == mv.ABAJO:
        fila_obj += 1
    elif direccion == mv.IZQUIERDA:
        columna_obj -= 1
    elif direccion == mv.DERECHA:
        columna_obj += 1
    else:
        print('No se reconoce la direccion')

    if fila_obj < 0 or columna_obj < 0 or fila_obj >= len(tablero) or columna_obj >= len(tablero[0]):
        print('Movimiento no válido')
        return

    if tablero[fila_obj][columna_obj] == board.SPACE:
        tablero[fila][columna] = board.SPACE
        tablero[fila_obj][columna_obj] = board.ROBOT

    elif tablero[fila_obj][columna_obj] == board.CAJA:
        fila_caja, columna_caja = fila_obj, columna_obj
        if direccion == mv.ARRIBA:
            fila_caja -= 1
        elif direccion == mv.ABAJO:
            fila_caja += 1
        elif direccion == mv.IZQUIERDA:
            columna_caja -= 1
        elif direccion == mv.DERECHA:
            columna_caja += 1

        if tablero[fila_caja][columna_caja] == board.SPACE or tablero[fila_caja][columna_caja] == board.DESTINO:
            if tablero[fila_caja][columna_caja] == board.DESTINO:
                tablero[fila_caja][columna_caja] = board.CAJA
                board.CAJA_MOVIBLE = False
            else:
                tablero[fila_caja][columna_caja] = board.CAJA

            tablero[fila_obj][columna_obj] = board.SPACE
            tablero[fila][columna] = board.SPACE
            tablero[fila_obj][columna_obj] = board.ROBOT

        else:
            print('Movimiento no válido: no puedes mover la caja allí.')

    else:
        print('Movimiento no válido')

def win(tablero):
    for fila in tablero:
        for columna in fila:
            if columna == board.SPACE:
                return False
    return True

def leer_direccion():
    direccion = input('Ingrese el movimiento (W/A/S/D) o X para salir: ')
    direccion = direccion.upper()
    if direccion == 'W':
        return mv.ARRIBA
    elif direccion == 'A':
        return mv.IZQUIERDA
    elif direccion == 'S':
        return mv.ABAJO
    elif direccion == 'D':
        return mv.DERECHA
    elif direccion == 'X':
        return mv.EXIT
    else:
        return leer_direccion()

def juego():
    tab = board.tablero
    imprimir_tablero(tab)
    direccion = leer_direccion()
    while direccion != mv.EXIT and not win(tab):
        mover_robot(tab, direccion)
        imprimir_tablero(tab)
        direccion = leer_direccion()
    if win(tab):
        print('¡Felicidades, has completado el tablero!')
    else:
        print('Chao')

def manual(idioma):
    menu_manual = {
        'es': {
            'desc': 'El juego consiste en recorrer todo el tablero.',
            board.ROBOT: 'Es el robot.',
            board.OBSTA: 'Es el obstáculo.',
            board.DESTINO: 'Es el destino, puedes caminar sobre él.',
            board.CAJA: 'Es la caja que el robot debe mover.'
        },
        'en': {
            'desc': 'You have to move around the full board.',
            board.ROBOT: 'This is the robot.',
            board.OBSTA: 'This is the obstacle.',
            board.DESTINO: 'This is the destination, you can walk over it.',
            board.CAJA: 'This is the box that the robot must move.'
        },
    }
    print(menu_manual[idioma]['desc'])
    for k, v in menu_manual[idioma].items():
        if k != 'desc':
            print(f'\t{k} - {v}')
    input('Presiona Enter para regresar al menú.')

def menu():
    mi_menu = {
        'es': {
            '1': 'Iniciar juego nuevo',
            '2': 'Ver manual de juego',
            '3': 'Salir'
        },
        'en': {
            '1': 'Start new game',
            '2': 'Show manual',
            '3': 'Exit'
        },
    }
    lang = input('Indique el idioma (en/es): ')
    if lang not in mi_menu:
        lang = 'es'
    while True:
        limpiar_pantalla()
        print('--------------------------------')
        for k, v in mi_menu[lang].items():
            print(f'{k}. {v}')
        print('--------------------------------')
        opt = input('Ingrese la opción deseada: ')
        if opt == '1':
            juego()
        elif opt == '2':
            manual(lang)
        elif opt == '3':
            print('Nos vemos la próxima.')
            break
        else:
            print('Opción no válida. Inténtalo de nuevo.')

menu()

