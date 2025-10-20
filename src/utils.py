from src.constants import TODAS_CARTAS
import random
from collections import defaultdict

random.seed(42)  # Reproducibilidad

def repartir_mano(cartas: list = TODAS_CARTAS, numero_cartas: int = 3, mis_cartas = None) -> list:
    if mis_cartas:
        mis_cartas_set = set(mis_cartas)
        mazo_disponible = [c for c in cartas if c not in mis_cartas_set]
    else:
        mazo_disponible = cartas

    if len(mazo_disponible) < numero_cartas:
        raise ValueError("No hay suficientes cartas disponibles para repartir.")

    return random.sample(mazo_disponible, k=numero_cartas)


def calcular_envido(mano: list) -> int:
    palos = defaultdict(list)
    for palo, carta in mano:
        valor = carta if carta <= 7 else 0
        palos[palo].append(valor)
    
    mejor = 0
    for valores in palos.values():
        if len(valores) >= 2:
            v_sorted = sorted(valores, reverse=True)
            total = v_sorted[0] + v_sorted[1] + 20
        else:
            total = valores[0]
        if total > mejor:
            mejor = total
    return mejor



def simular_envidos_list(mis_cartas: list, numero_simulaciones: int = 10000) -> list:
    envidos_oponente = []
    for _ in range(numero_simulaciones):
        mano_oponente = repartir_mano(TODAS_CARTAS, 3, mis_cartas)
        envido_oponente = calcular_envido(mano_oponente)
        envidos_oponente.append(envido_oponente)
    return envidos_oponente


def simular_envido(mis_cartas: list, numero_simulaciones: int = 10000) -> float:
    victorias = 0
    mi_envido = calcular_envido(mis_cartas)
    for _ in range(numero_simulaciones):
        mano_oponente = repartir_mano(mis_cartas, TODAS_CARTAS)
        envido_oponente = calcular_envido(mano_oponente)
        if mi_envido > envido_oponente:
            victorias += 1
    probabilidad_ganar = victorias / numero_simulaciones
    return probabilidad_ganar


