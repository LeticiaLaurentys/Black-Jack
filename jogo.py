import random  # Biblioteca para embaralhar cartas

# Lista de naipes e valores das cartas
naipes = ['Copas', 'Espadas', 'Ouros', 'Paus']
valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

# Função para exibir cartas em um formato legível
def exibir_mao(mao):
    return ', '.join([f"{valor} de {naipe}" for valor, naipe in mao])

# Criar e embaralhar um novo baralho
def criar_baralho():
    baralho = [(valor, naipe) for valor in valores for naipe in naipes]
    random.shuffle(baralho)
    return baralho

# Distribuir cartas para jogadores
def distribuir_cartas(baralho, num_cartas=2):
    return [baralho.pop() for _ in range(num_cartas)]

# Calcular pontuação da mão (Ás pode valer 1 ou 11)
def calcular_valor_mao(mao):
    valor_total = 0
    num_ases = 0

    for carta in mao:
        valor = carta[0]
        if valor in ['J', 'Q', 'K']:  # Cartas de figura valem 10
            valor_total += 10
        elif valor == 'A':  # Ás vale 11, mas pode ser ajustado para 1
            valor_total += 11
            num_ases += 1
        else:
            valor_total += int(valor)

    while valor_total > 21 and num_ases:  # Ajusta Ás para evitar estouro
        valor_total -= 10
        num_ases -= 1

    return valor_total

# Verifica vencedor comparando apenas os jogadores
def verificar_vencedor(jogadores):
    pontuacoes = {jogador: calcular_valor_mao(mao) for jogador, mao in jogadores.items()}
    pontuacoes_validas = {jogador: pontos for jogador, pontos in pontuacoes.items() if pontos <= 21}

    if not pontuacoes_validas:
        return "Todos estouraram! Não há vencedor."

    vencedor = max(pontuacoes_validas, key=pontuacoes_validas.get)
    return f"Vencedor: {vencedor} com {pontuacoes_validas[vencedor]} pontos!"
