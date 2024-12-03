
import tkinter as tk
from tkinter import messagebox
from jogo_base import criar_baralho, distribuir_cartas, calcular_valor_mao, verificar_vencedor, turno_dealer

class InterfaceBlackjack:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack - 21")
        self.root.geometry("600x400")
        
        self.baralho = []
        self.mao_jogador = []
        self.mao_dealer = []
        self.dificuldade = 'facil'
        
        self.info_label = tk.Label(self.root, text="Bem-vindo ao Blackjack!", font=("Arial", 14))
        self.info_label.pack(pady=10)
        
        self.mao_jogador_label = tk.Label(self.root, text="Sua mão: ", font=("Arial", 12))
        self.mao_jogador_label.pack(pady=5)
        
        self.dealer_label = tk.Label(self.root, text="Mão do dealer: ", font=("Arial", 12))
        self.dealer_label.pack(pady=5)
        
        self.pontuacao_label = tk.Label(self.root, text="Pontuação: 0", font=("Arial", 12))
        self.pontuacao_label.pack(pady=5)
        
        self.actions_frame = tk.Frame(self.root)
        self.actions_frame.pack(pady=10)
        
        self.pedir_button = tk.Button(self.actions_frame, text="Pedir Carta", command=self.pedir_carta)
        self.pedir_button.pack(side=tk.LEFT, padx=5)
        
        self.parar_button = tk.Button(self.actions_frame, text="Parar", command=self.parar)
        self.parar_button.pack(side=tk.LEFT, padx=5)
        
        self.reiniciar_button = tk.Button(self.root, text="Reiniciar Jogo", command=self.reiniciar)
        self.reiniciar_button.pack(pady=10)
        
        self.reiniciar()
    
    def reiniciar(self):
        self.baralho = criar_baralho()
        self.mao_jogador = distribuir_cartas(self.baralho)
        self.mao_dealer = distribuir_cartas(self.baralho)
        self.atualizar_interface()
        self.info_label.config(text="Escolha sua ação")
        self.pedir_button.config(state=tk.NORMAL)
        self.parar_button.config(state=tk.NORMAL)
    
    def atualizar_interface(self):
        self.mao_jogador_label.config(text=f"Sua mão: {', '.join([f'{c[0]} de {c[1]}' for c in self.mao_jogador])}")
        self.dealer_label.config(text=f"Cartas do dealer: {self.mao_dealer[0][0]} de {self.mao_dealer[0][1]}, ?")
        self.pontuacao_label.config(text=f"Pontuação: {calcular_valor_mao(self.mao_jogador)}")
    
    def pedir_carta(self):
        if calcular_valor_mao(self.mao_jogador) >= 21:
            self.info_label.config(text="Você não pode pedir mais cartas!")
            return
        
        self.mao_jogador.append(self.baralho.pop())
        self.atualizar_interface()
        
        if calcular_valor_mao(self.mao_jogador) > 21:
            self.info_label.config(text="Você estourou! Dealer venceu.")
            self.pedir_button.config(state=tk.DISABLED)
            self.parar_button.config(state=tk.DISABLED)
    
    def parar(self):
        self.pedir_button.config(state=tk.DISABLED)
        self.parar_button.config(state=tk.DISABLED)
        
        turno_dealer(self.baralho, self.mao_dealer, self.dificuldade)
        resultado = verificar_vencedor(self.mao_jogador, self.mao_dealer)
        
        self.dealer_label.config(text=f"Mão do dealer: {', '.join([f'{c[0]} de {c[1]}' for c in self.mao_dealer])}")
        self.info_label.config(text=resultado)
        self.pontuacao_label.config(text=f"Pontuação final: {calcular_valor_mao(self.mao_jogador)}")
        messagebox.showinfo("Resultado", resultado)
