import tkinter as tk
from PIL import Image, ImageTk
import random
from jogo import criar_baralho, distribuir_cartas, exibir_mao, calcular_valor_mao, verificar_vencedor

class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack 21")

        # Carregar imagem de fundo
        self.bg_image = Image.open("background.jpg")
        self.bg_image = self.bg_image.resize((800, 600))  
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Criar o Canvas para exibir a imagem de fundo
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Saldo inicial e estatísticas
        self.saldo = 1000  
        self.saldo_dealer = 1000  # Saldo inicial do Dealer
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0

        # Perguntar nome do jogador
        self.label_nome = tk.Label(root, text="Seu nome:", font=("Arial", 14), bg="black", fg="white")
        self.label_nome_window = self.canvas.create_window(400, 150, window=self.label_nome)

        self.entry_nome = tk.Entry(root, font=("Arial", 14))
        self.entry_nome_window = self.canvas.create_window(400, 200, window=self.entry_nome)

        self.btn_confirmar_nome = tk.Button(root, text="Confirmar", command=self.definir_nome)
        self.btn_confirmar_nome_window = self.canvas.create_window(400, 250, window=self.btn_confirmar_nome)

        # Criar área de exibição das cartas, saldo e estatísticas
        self.texto_cartas = self.canvas.create_text(400, 300, text="", font=("Arial", 16), fill="white")
        self.texto_saldo = self.canvas.create_text(400, 50, text=f"Saldo: R$ {self.saldo}", font=("Arial", 14), fill="yellow")
        self.texto_saldo_dealer = self.canvas.create_text(400, 75, text=f"Saldo Dealer: R$ {self.saldo_dealer}", font=("Arial", 12), fill="red")
        self.texto_stats = self.canvas.create_text(400, 100, text="", font=("Arial", 12), fill="cyan")

        # Criar botões de ação (escondidos inicialmente)
        self.btn_hit = tk.Button(root, text="Comprar Carta (Hit)", command=self.comprar_carta)
        self.btn_stand = tk.Button(root, text="Parar (Stand)", command=self.parar_jogo)
        self.btn_double_down = tk.Button(root, text="Double Down", command=self.double_down)
        self.btn_reiniciar = tk.Button(root, text="Reiniciar Jogo", command=self.reiniciar_jogo)
        



        self.btn_hit_window = self.canvas.create_window(200, 500, window=self.btn_hit)
        self.btn_stand_window = self.canvas.create_window(400, 500, window=self.btn_stand)
        self.btn_double_down_window = self.canvas.create_window(600, 500, window=self.btn_double_down)
        self.btn_reiniciar_window = self.canvas.create_window(400, 550, window=self.btn_reiniciar)

        self.canvas.itemconfig(self.btn_hit_window, state="hidden")
        self.canvas.itemconfig(self.btn_stand_window, state="hidden")
        self.canvas.itemconfig(self.btn_double_down_window, state="hidden")
        self.canvas.itemconfig(self.btn_reiniciar_window, state="hidden")

    def definir_nome(self):
        self.nome_jogador = self.entry_nome.get().strip()
        if not self.nome_jogador:
            self.nome_jogador = "Você"

        # Esconder entrada de nome
        self.canvas.itemconfig(self.label_nome_window, state="hidden")
        self.canvas.itemconfig(self.entry_nome_window, state="hidden")
        self.canvas.itemconfig(self.btn_confirmar_nome_window, state="hidden")

       
        # Esconde as cartas para reiniciar a rodada
        self.canvas.itemconfig(self.texto_cartas, text="")


        # Volta para a tela de aposta
        self.perguntar_aposta()


    def perguntar_aposta(self):
        if self.saldo <= 0:
            self.finalizar_jogo("Você está sem saldo! Jogo encerrado.")
            return

        self.label_aposta = tk.Label(root, text="Quanto deseja apostar?", font=("Arial", 14), bg="black", fg="white")
        self.label_aposta_window = self.canvas.create_window(400, 200, window=self.label_aposta)

        self.entry_aposta = tk.Entry(root, font=("Arial", 14))
        self.entry_aposta_window = self.canvas.create_window(400, 250, window=self.entry_aposta)

        self.btn_confirmar_aposta = tk.Button(root, text="Apostar", command=self.definir_aposta)
        self.btn_confirmar_aposta_window = self.canvas.create_window(400, 300, window=self.btn_confirmar_aposta)

    def definir_aposta(self):
        try:
            self.aposta = int(self.entry_aposta.get())
            if self.aposta < 1 or self.aposta > self.saldo:
                raise ValueError("Aposta inválida")

            self.saldo -= self.aposta  # Retirar aposta do saldo do jogador

            # **Definir a aposta do Dealer aleatoriamente**
            min_aposta = int(self.aposta * 0.5)  # 50% do valor do jogador
            max_aposta = int(self.aposta * 1.5)  # 150% do valor do jogador
            self.aposta_dealer = random.randint(min_aposta, max_aposta)

            # Se a aposta do Dealer for maior que seu saldo, ele aposta tudo o que tem
            if self.aposta_dealer > self.saldo_dealer:
                self.aposta_dealer = self.saldo_dealer

            self.saldo_dealer -= self.aposta_dealer  # Reduzir saldo do Dealer

            # Atualizar os saldos na interface
            self.canvas.itemconfig(self.texto_saldo, text=f"Saldo: R$ {self.saldo}")
            self.canvas.itemconfig(self.texto_saldo_dealer, text=f"Saldo Dealer: R$ {self.saldo_dealer}")

            # Esconder entrada de aposta
            self.canvas.itemconfig(self.label_aposta_window, state="hidden")
            self.canvas.itemconfig(self.entry_aposta_window, state="hidden")
            self.canvas.itemconfig(self.btn_confirmar_aposta_window, state="hidden")

            if hasattr(self, 'btn_iniciar_window'):  # Se o botão já existir, apenas reativa
                self.canvas.itemconfig(self.btn_iniciar_window, state="normal")
            else:  # Se ainda não foi criado, cria o botão
                self.btn_iniciar = tk.Button(self.root, text="Iniciar Jogo", command=self.iniciar_jogo)
                self.btn_iniciar_window = self.canvas.create_window(400, 350, window=self.btn_iniciar)

        except ValueError:
            self.entry_aposta.delete(0, tk.END)
            self.entry_aposta.insert(0, "Valor inválido!")

    def iniciar_jogo(self):
        self.baralho = criar_baralho()
        self.jogadores = {self.nome_jogador: distribuir_cartas(self.baralho)}
        self.jogadores["Dealer"] = distribuir_cartas(self.baralho)  # O croupier

        self.atualizar_tela()

        # Esconder botão de iniciar e mostrar botões de ação
        self.canvas.itemconfig(self.btn_iniciar_window, state="hidden")
        self.canvas.itemconfig(self.btn_hit_window, state="normal")
        self.canvas.itemconfig(self.btn_stand_window, state="normal")
        self.canvas.itemconfig(self.btn_double_down_window, state="normal")

        self.jogo_em_andamento = True

    def atualizar_tela(self):
        # Mostrar as cartas de todos os jogadores
        cartas_texto = "\n".join([f"{jogador}: {exibir_mao(mao)} - {calcular_valor_mao(mao)} pontos"
                                  for jogador, mao in self.jogadores.items()])
        self.canvas.itemconfig(self.texto_cartas, text=cartas_texto)

    def comprar_carta(self):
        if not self.jogo_em_andamento:
            return

        self.jogadores[self.nome_jogador].append(self.baralho.pop())
        self.atualizar_tela()

        if calcular_valor_mao(self.jogadores[self.nome_jogador]) > 21:
            self.finalizar_jogo()

    def double_down(self):
        if not self.jogo_em_andamento:
            return
    
        if self.aposta * 2 > self.saldo:  # Impede que o jogador use Double Down se não tiver saldo suficiente
            return
    
        self.saldo -= self.aposta  # Dobra a aposta
        self.aposta *= 2
        self.canvas.itemconfig(self.texto_saldo, text=f"Saldo: R$ {self.saldo}")

        self.comprar_carta()  # O jogador recebe apenas mais uma carta
        self.parar_jogo()  # Dealer joga automaticamente após Double Down


    def parar_jogo(self):
        self.jogada_do_dealer()

    def jogada_do_dealer(self):
        while calcular_valor_mao(self.jogadores["Dealer"]) < 17:
            self.jogadores["Dealer"].append(self.baralho.pop())

        self.finalizar_jogo()

    def finalizar_jogo(self, mensagem=""):
        vencedor = verificar_vencedor(self.jogadores)
        self.atualizar_estatisticas(vencedor)

        # Atualizar interface com os resultados da rodada
        self.canvas.itemconfig(self.texto_cartas, text=f"{mensagem}\n{vencedor}\nSaldo final: R$ {self.saldo}")

        # Atualizar estatísticas na interface
        stats_text = f"Vitórias: {self.vitorias} | Derrotas: {self.derrotas} | Empates: {self.empates}"
        self.canvas.itemconfig(self.texto_stats, text=stats_text)

        # Verificar se o saldo do jogador ou do dealer chegou a zero
        if self.saldo <= 0:
            self.canvas.itemconfig(self.texto_cartas, text="💀 VOCÊ PERDEU! Seu saldo zerou! O dealer venceu. 💀")
            self.encerrar_jogo()
            return
        elif self.saldo_dealer <= 0:
            self.canvas.itemconfig(self.texto_cartas, text="🏆 PARABÉNS! Você zerou o saldo do Dealer e venceu o jogo! 🏆")
            self.encerrar_jogo()
            return

        # Esconder botões de ação
        self.canvas.itemconfig(self.btn_hit_window, state="hidden")
        self.canvas.itemconfig(self.btn_stand_window, state="hidden")
        self.canvas.itemconfig(self.btn_double_down_window, state="hidden")

        # Se o saldo for positivo, exibir botão de reinício normalmente
        if self.saldo > 0:
            self.canvas.itemconfig(self.btn_reiniciar_window, state="normal")

        self.jogo_em_andamento = False


    def encerrar_jogo(self):
        """ Finaliza completamente o jogo e impede novas rodadas. """
        self.canvas.itemconfig(self.texto_stats, text="JOGO FINALIZADO! Obrigado por jogar. 🎰")

        # Esconder todos os botões
        self.canvas.itemconfig(self.btn_hit_window, state="hidden")
        self.canvas.itemconfig(self.btn_stand_window, state="hidden")
        self.canvas.itemconfig(self.btn_double_down_window, state="hidden")
        self.canvas.itemconfig(self.btn_reiniciar_window, state="hidden")

        # Criar botão para fechar o jogo
        self.btn_sair = tk.Button(self.root, text="Sair do Jogo", command=self.root.quit)
        self.btn_sair_window = self.canvas.create_window(400, 550, window=self.btn_sair)


    def atualizar_estatisticas(self, vencedor):
        if self.nome_jogador in vencedor:
            self.vitorias += 1
            self.saldo += self.aposta * 2
        elif "Empate" in vencedor:
            self.empates += 1
            self.saldo += self.aposta  # Recupera a aposta em caso de empate
        else:
            self.derrotas += 1

    def reiniciar_jogo(self):
        # Atualiza saldo e estatísticas
        self.canvas.itemconfig(self.texto_saldo, text=f"Saldo: R$ {self.saldo}")
        self.canvas.itemconfig(self.texto_stats, text=f"Vitórias: {self.vitorias} | Derrotas: {self.derrotas} | Empates: {self.empates}")
        self.canvas.itemconfig(self.texto_cartas, text="")

         #Esconde botões de ação e empréstimo
        self.canvas.itemconfig(self.btn_reiniciar_window, state="hidden")

        # Exibe novamente a opção de apostar
        self.perguntar_aposta()



if __name__ == "__main__":
    root = tk.Tk()
    gui = BlackjackGUI(root)
    root.mainloop()
