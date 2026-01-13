from src.constants import TODAS_CARTAS
import random
import pandas as pd
from collections import defaultdict

random.seed(42)

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


def simulacion_completa(numero_simulaciones: int = 10000) -> pd.DataFrame:
    envidos_oponente = []
    cartas_oponente = []
    mis_envidos = []
    mis_cartas = []
    victorias = []
    soy_manos = []
    
    for i in range(numero_simulaciones):
        
        soy_mano = (i % 2 == 0) # par, por ejemplo

        if soy_mano:
            mi_mano = repartir_mano(TODAS_CARTAS, 3)
            mano_oponente = repartir_mano(TODAS_CARTAS, 3, mi_mano)
        else:
            mano_oponente = repartir_mano(TODAS_CARTAS, 3)
            mi_mano = repartir_mano(TODAS_CARTAS, 3, mano_oponente)

        mi_envido = calcular_envido(mi_mano)
        envido_oponente = calcular_envido(mano_oponente)

        if mi_envido > envido_oponente:
            victoria = True
        elif mi_envido < envido_oponente:
            victoria = False
        else:
            victoria = soy_mano  # empate lo gana mano
        
        # acumulo
        envidos_oponente.append(envido_oponente)
        cartas_oponente.append(mano_oponente)
        mis_envidos.append(mi_envido)
        mis_cartas.append(mi_mano)
        soy_manos.append(soy_mano)
        victorias.append(victoria)
    
    return pd.DataFrame({
        "envido_oponente": envidos_oponente,
        "mano_oponente": cartas_oponente,
        "mi_envido": mis_envidos,
        "mi_mano": mis_cartas,
        "soy_mano": soy_manos,
        "victoria": victorias
    })
