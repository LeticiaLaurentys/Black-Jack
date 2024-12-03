
# Jogo blackjack / 21 em python
# Autor: Leticia Laurentys e Matheus Rodrigues
# Data início: 07/10/2024  Data final:

import random

naipes = ['Copas', 'Espadas', 'Ouros', 'Paus']
valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

def exibir_mao(mao):
    return ', '.join([f"{valor} de {naipe}" for valor, naipe in mao])

def criar_baralho():
    baralho = [(valor, naipe) for valor in valores for naipe in naipes]
    random.shuffle(baralho)  
    return baralho

def distribuir_cartas(baralho, num_cartas=2):
    return [baralho.pop() for _ in range(num_cartas)]

def calcular_valor_mao(mao):
    valor_total = 0
    num_ases = 0
    for carta in mao:
        valor = carta[0]
        if valor in ['J', 'Q', 'K']:
            valor_total += 10
        elif valor == 'A':
            valor_total += 11
            num_ases += 1
        else:
            valor_total += int(valor)
    
    while valor_total > 21 and num_ases:
        valor_total -= 10
        num_ases -= 1
    
    return valor_total

def verificar_vencedor(mao_jogador, mao_dealer):
    valor_jogador = calcular_valor_mao(mao_jogador)
    valor_dealer = calcular_valor_mao(mao_dealer)
    
    if valor_jogador > 21:
        return "Dealer venceu, jogador estourou!"
    elif valor_dealer > 21:
        return "Jogador venceu, dealer estourou!"
    elif valor_jogador > valor_dealer:
        return "Jogador venceu!"
    elif valor_dealer > valor_jogador:
        return "Dealer venceu!"
    else:
        return "Empate!"

def decisao_ia(mao_dealer, dificuldade):
    valor_mao = calcular_valor_mao(mao_dealer)

    if dificuldade == 'facil':
        return 'parar' if valor_mao >= 15 else 'pedir'
    elif dificuldade == 'medio':
        if valor_mao < 12:
            return 'pedir'
        elif 12 <= valor_mao <= 16:
            return 'pedir'
        else:
            return 'parar'
    elif dificuldade == 'dificil':
        if random.random() < 0.7:  
            if valor_mao < 12:
                return 'pedir'
            elif 12 <= valor_mao <= 16:
                return 'pedir'
            else:
                return 'parar'
        else:
            return 'pedir'  

def turno_dealer(baralho, mao_dealer, dificuldade):
    while True:
        acao = decisao_ia(mao_dealer, dificuldade)  
        if acao == 'pedir':
            mao_dealer.append(baralho.pop())
            if calcular_valor_mao(mao_dealer) > 21:  
                break
        elif acao == 'parar':
            break
