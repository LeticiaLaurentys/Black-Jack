import tkinter as tk
from tkinter import messagebox
from jogo import criar_baralho, distribuir_cartas, calcular_valor_mao, exibir_mao, turno_dealer, verificar_vencedor

class InterfaceBlackjack:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo 21")
        self.root.geometry("400x400")

        # Variáveis principais
        self.baralho = []
        self.mao_jogador = []
        self.mao_dealer = []
        self.dificuldade = None

        # Frames principais
        self.frame_dificuldade = tk.Frame(root)
        self.frame_jogo = tk.Frame(root)

        # Frame de dificuldade
        self.iniciar_frame_dificuldade()

        # Widgets do frame do jogo
        self.label_mao_jogador = tk.Label(self.frame_jogo, text="", wraplength=350)
        self.label_mao_jogador.pack(pady=10)

        self.label_pergunta = tk.Label(self.frame_jogo, text="", wraplength=350)
        self.label_pergunta.pack(pady=5)

        self.botao_pedir = tk.Button(self.frame_jogo, text="Pedir Carta", command=self.pedir_carta)
        self.botao_parar = tk.Button(self.frame_jogo, text="Parar", command=self.parar_jogo)

    def iniciar_frame_dificuldade(self):
        # Gerencia o frame de dificuldade
        self.frame_jogo.pack_forget()  # Esconde o frame do jogo (se estiver visível)
        self.frame_dificuldade.pack(pady=20)

        label = tk.Label(self.frame_dificuldade, text="Escolha o nível de dificuldade:")
        label.pack()

        # Botões lado a lado
        dificuldades = ["Fácil", "Médio", "Difícil"]
        for nivel in dificuldades:
            botao = tk.Button(
                self.frame_dificuldade,
                text=nivel,
                command=lambda n=nivel.lower(): self.iniciar_jogo(n),
                width=10,
            )
            botao.pack(side="left", padx=5)

    def iniciar_jogo(self, dificuldade):
        # Inicializa as variáveis do jogo
        self.dificuldade = dificuldade
        self.baralho = criar_baralho()
        self.mao_jogador = distribuir_cartas(self.baralho)
        self.mao_dealer = distribuir_cartas(self.baralho)

        # Atualizar a interface
        self.frame_dificuldade.pack_forget()  # Esconde os botões de dificuldade
        self.frame_jogo.pack(pady=20)
        self.atualizar_mao_jogador()
        self.label_pergunta.config(text="Deseja pedir carta ou parar?")
        self.botao_pedir.pack(side="left", padx=10)
        self.botao_parar.pack(side="left", padx=10)

    def atualizar_mao_jogador(self):
        texto_mao = f"Sua mão: {exibir_mao(self.mao_jogador)}\nPontuação: {calcular_valor_mao(self.mao_jogador)}"
        self.label_mao_jogador.config(text=texto_mao)

    def pedir_carta(self):
        self.mao_jogador.append(self.baralho.pop())
        self.atualizar_mao_jogador()

        if calcular_valor_mao(self.mao_jogador) > 21:
            messagebox.showinfo("Resultado", "Você estourou! Dealer venceu.")
            self.reiniciar_jogo()

    def parar_jogo(self):
        # Turno do dealer
        turno_dealer(self.mao_dealer, self.baralho, self.dificuldade)
        resultado = verificar_vencedor(self.mao_jogador, self.mao_dealer)
        self.exibir_resultado_final(resultado)

    def exibir_resultado_final(self, resultado):
        # Exibir mãos finais e resultado
        mao_jogador_str = f"Sua mão final: {exibir_mao(self.mao_jogador)}\nPontuação: {calcular_valor_mao(self.mao_jogador)}"
        mao_dealer_str = f"Mão final do dealer: {exibir_mao(self.mao_dealer)}\nPontuação: {calcular_valor_mao(self.mao_dealer)}"
        resultado_str = f"{mao_jogador_str}\n\n{mao_dealer_str}\n\n{resultado}"

        messagebox.showinfo("Resultado Final", resultado_str)
        self.reiniciar_jogo()

    def reiniciar_jogo(self):
        # Limpa as variáveis e volta para a escolha de dificuldade
        self.mao_jogador = []
        self.mao_dealer = []
        self.baralho = []
        self.dificuldade = None

        self.frame_jogo.pack_forget()
        self.iniciar_frame_dificuldade()


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBlackjack(root)
    root.mainloop()
