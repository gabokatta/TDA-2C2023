import argparse
import random

def extract_jugadores(path):
    file = open(path, 'r')
    data = file.read()
    lines = data.splitlines()
    jugadores = set()
    pedidos_prensa = [set(line.strip().split(',')) for line in lines]
    for conjunto in pedidos_prensa:
        for jugador in conjunto:
            jugadores.add(jugador)
    return list(jugadores)


def generate_pedidos(jugadores, n_pedidos):
    new_pedidos = []
    for i in range(n_pedidos):
        pedido_size = random.randint(1, (len(jugadores)//2))
        selected = random.sample(jugadores, k=pedido_size)
        new_pedidos.append(selected)
    return new_pedidos


def main():
    parser = argparse.ArgumentParser(description="Generate random lines and write them to a file.")
    parser.add_argument("jugadores_path", help="Path to the pedidos file of players to sample.")
    parser.add_argument("n_pedidos", type=int, help="Number of pedidos to generate")

    args = parser.parse_args()
    
    path = args.jugadores_path
    n_pedidos = args.n_pedidos

    jugadores = extract_jugadores(path)
    
    for pedido in generate_pedidos(jugadores, n_pedidos):
        print(pedido)
    print(f"Unique Player Amount: {len(jugadores)}")

if __name__ == "__main__":
    main()