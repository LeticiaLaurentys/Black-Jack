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
            return 'pedir' if valor_mao < 7 else 'parar'
        else:
            return 'parar'
    
    elif dificuldade == 'dificil':
        #
        if random.random() < 0.7:  
            if valor_mao < 12:
                return 'pedir'
            elif 12 <= valor_mao <= 16:
                return 'pedir' if valor_mao < 7 else 'parar'
            else:
                return 'parar'
        else:
            return 'pedir'  


def turno_dealer(baralho, mao_dealer, dificuldade):
    while True:
        acao = decisao_ia(mao_dealer, dificuldade)  
        if acao == 'pedir':
            mao_dealer.append(baralho.pop())
            print(f"O dealer pediu uma carta: {exibir_mao([mao_dealer[-1]])}")
            if calcular_valor_mao(mao_dealer) > 21:  
                print("Dealer estourou!")
                break
        elif acao == 'parar':
            break
    print(f"Mão final do dealer: {exibir_mao(mao_dealer)} - Pontuação: {calcular_valor_mao(mao_dealer)}")


def exibir_resultado(mao_jogador, mao_dealer):
    valor_jogador = calcular_valor_mao(mao_jogador)
    valor_dealer = calcular_valor_mao(mao_dealer)
    
    print(f"Sua mão final: {exibir_mao(mao_jogador)} - Pontuação: {valor_jogador}")
    print(f"Mão final do dealer: {exibir_mao(mao_dealer)} - Pontuação: {valor_dealer}")
    
    
    resultado = verificar_vencedor(mao_jogador, mao_dealer)
    print(resultado)


def turno_jogador(baralho, mao_jogador):
    while True:
        print(f"Sua mão: {exibir_mao(mao_jogador)} - Pontuação: {calcular_valor_mao(mao_jogador)}")
        escolha = input("Deseja pedir carta ou parar? (pedir/parar): ").strip().lower()
        
        if escolha == 'pedir':
            mao_jogador.append(baralho.pop())
            if calcular_valor_mao(mao_jogador) > 21:  
                print("Você estourou!")
                break
        elif escolha == 'parar':
            break
        else:
            print("Opção inválida. Tente novamente.")


def jogar():
    while True:  
        
        dificuldade = input("Escolha o nível de dificuldade (facil/medio/dificil): ").lower()
        while dificuldade not in ['facil', 'medio', 'dificil']:
            print("Nível inválido. Tente novamente.")
            dificuldade = input("Escolha o nível de dificuldade (facil/medio/dificil): ").lower()
        
        
        baralho = criar_baralho()
        
        
        mao_jogador = distribuir_cartas(baralho)
        mao_dealer = distribuir_cartas(baralho)
        
        
        carta_dealer = mao_dealer[0]
        print(f"A carta do dealer: {exibir_mao([carta_dealer])}")  
        
        
        turno_jogador(baralho, mao_jogador)
        
        
        if calcular_valor_mao(mao_jogador) <= 21:
            turno_dealer(baralho, mao_dealer, dificuldade)
        
        
        exibir_resultado(mao_jogador, mao_dealer)

        
        jogar_novamente = input("Deseja jogar novamente? (s/n): ").strip().lower()
        if jogar_novamente != 's':
            print("Obrigado por jogar!")
            break


jogar()