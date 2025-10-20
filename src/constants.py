PALOS = ["Basto", "Copa", "Espada", "Oro"]
CARTAS = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
NUMERO_CARTAS = len(PALOS) * len(CARTAS)
TODAS_CARTAS = [(palo, carta) for palo in PALOS for carta in CARTAS]

print(TODAS_CARTAS)