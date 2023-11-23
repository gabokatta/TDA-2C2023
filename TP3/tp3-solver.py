import argparse
import time
from pulp import LpProblem, LpVariable, LpSolverDefault, lpSum, LpMinimize

def backtracking(jugadores, pedidos):
    return seleccion_backtracking(jugadores, pedidos, [], jugadores.copy())
    

def seleccion_backtracking(jugadores, pedidos, actual, final):
    if not pedidos:
        if len(actual) < len(final):
            final = actual[:]
        return final

    for i, jugador_actual in enumerate(jugadores):

        if len(actual) + 1 >= len(final):
            break

        if jugador_actual not in actual:
            actual.append(jugador_actual)
            nuevos_pedidos = [conjunto for conjunto in pedidos if jugador_actual not in conjunto]
            final = seleccion_backtracking(jugadores[i+1:], nuevos_pedidos, actual, final)
            actual.pop()

    return final


def linear(jugadores, pedidos):
    LpSolverDefault.msg = 0
    prob = LpProblem("SeleccionJugadores", LpMinimize)

    x = {jugador: LpVariable(name=f"x_{jugador}", cat="Binary") for jugador in jugadores}

    prob += lpSum(x[jugador] for jugador in jugadores)

    for conjunto in pedidos:
        prob += lpSum(x[jugador] for jugador in conjunto) >= 1

    prob.solve()

    seleccion_final = {jugador: int(x[jugador].value()) for jugador in jugadores}

    return seleccion_final

def linear_approx(jugadores, pedidos):
    LpSolverDefault.msg = 0
    prob = LpProblem("SeleccionJugadores", LpMinimize)

    x = {jugador: LpVariable(name=f"x_{jugador}", lowBound=0, upBound=1) for jugador in jugadores}

    prob += lpSum(x[jugador] for jugador in jugadores)

    for conjunto in pedidos:
        prob += lpSum(x[jugador] for jugador in conjunto) >= 1

    prob.solve()

    # Redondear el resultado final
    b = max(len(conjunto) for conjunto in pedidos)
    for jugador in jugadores:
        valor_relajado = x[jugador].value()
        x[jugador].value = 1 if valor_relajado >= 1 / b else 0

    seleccion_final = {jugador: int(x[jugador].value) for jugador in jugadores}

    return seleccion_final

# Ordenamiento Greedy por Frecuencia de aparicion en los pedidos
def sort_jugadores_por_frecuencia(pedidos):
    freq = {}
    for conjunto in pedidos:
        for jugador in conjunto:
            freq[jugador] = freq.get(jugador, 0) + 1
    return sorted(freq.keys(), key=lambda jugador: freq[jugador], reverse=True)

def greedy(jugadores, pedidos):
    seleccion_final = []
    jugadores_ordenados = sort_jugadores_por_frecuencia(pedidos)

    for jugador in jugadores_ordenados:

      if not pedidos:
        break

      pedidos_pendientes = [pedido for pedido in pedidos if jugador in pedido]
      if pedidos_pendientes:
        seleccion_final.append(jugador)
        pedidos = [pedido for pedido in pedidos if jugador not in pedido]

    return seleccion_final

implementations = {
        "backtracking": backtracking,
        "linear": linear,
        "linear-aprox": linear_approx,
        "greedy": greedy,
}

def get_jugadores_pedidos_from_txt(path):
    file = open(path, 'r')
    data = file.read()
    lines = data.splitlines()
    jugadores = set()
    pedidos_prensa = [set(line.strip().split(',')) for line in lines]
    for conjunto in pedidos_prensa:
        for jugador in conjunto:
            jugadores.add(jugador)
    return (list(jugadores), pedidos_prensa)

def main():
    parser = argparse.ArgumentParser(description="Process a file in different execution modes.")
    parser.add_argument("file_name", help="Name of the file to process")
    parser.add_argument("--mode", default="linear", choices=["backtracking", "linear", "linear-aprox", "greedy"], help="Execution mode")
    args = parser.parse_args()
    mode = args.mode
    if mode not in implementations:
        print("Error: Invalid execution mode.")
        return
    
    jugadores, pedidos = get_jugadores_pedidos_from_txt(args.file_name)

    start = time.time()
    selection = implementations[mode](jugadores, pedidos)
    end = time.time()

    print(f"Execution Mode: {mode}")
    print(f"Time Taken: {(end-start):.6f}s")
    if (mode in ("linear", "linear-aprox")):
        print(f"Minimum Player Set: {[player for player in selection.keys() if selection[player] == 1]}")
        print(f"Set Size: {sum(selection.values())}")
    else:
        print(f"Minimum Player Set: {selection}")
        print(f"Set Size: {len(selection)}")


if __name__ == "__main__":
    main()