# src/gui/interface_pygame.py
# Interface gráfica completa do Paciência Yukon com Pygame
# Funciona com pack de cartas do GitHub: https://github.com/hanhaechi/playing-cards
# Inclui: imagens reais, botão novo jogo, arrastar/soltar, vitória

import pygame
import sys
import os
from src.game.jogo_yukon import JogoYukon

# ===================================================================
# CONFIGURAÇÕES DA TELA E CARTAS
# ===================================================================
LARGURA_TELA = 1200
ALTURA_TELA = 800
FPS = 60

# Cores (RGB)
VERDE_MESA = (0, 100, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (220, 20, 60)
DESTAQUE = (255, 255, 0, 80)  # Amarelo translúcido para arraste

# Dimensões das cartas
LARGURA_CARTA = 80
ALTURA_CARTA = 116
ESPACO_HORIZONTAL = 110
MARGEM_ESQUERDA = 80
MARGEM_TOPO = 160
SOBREPOSICAO = 30  # Distância entre cartas empilhadas

# Posições das fundações
FUNDOES_X_INICIAL = 580
FUNDOES_Y = 30

# Botão "NOVO JOGO"
BOTAO_X, BOTAO_Y = 50, 50
BOTAO_LARGURA, BOTAO_ALTURA = 180, 50

# ===================================================================
# CLASSE PRINCIPAL DA INTERFACE
# ===================================================================
class InterfacePygame:
    def __init__(self):
        # Inicializa Pygame
        pygame.init()
        pygame.display.set_caption("Paciência Yukon - Silvia Brandão 2025.2")
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.clock = pygame.time.Clock()

        # Fontes
        self.fonte = pygame.font.SysFont("Arial", 24, bold=True)
        self.fonte_pequena = pygame.font.SysFont("Arial", 18)
        self.fonte_vitoria = pygame.font.SysFont("Arial", 48, bold=True)

        # Carrega imagens das cartas
        self.imagens_cartas = self.carregar_imagens()

        # Estado do jogo
        self.jogo = JogoYukon()

        # Estado do arraste
        self.arrastando = False
        self.subpilha_arrastada = []
        self.origem_coluna = None
        self.origem_indice = None
        self.offset_x = 0
        self.offset_y = 0

    # ------------------------------------------------------------------
    # MÉTODO: carregar_imagens
    # Carrega imagens do pack GitHub (back.png + 1H.png, 2D.png, etc.)
    # ------------------------------------------------------------------
    def carregar_imagens(self):
        imagens = {}
        pasta = "cartas"
        if not os.path.exists(pasta):
            print("AVISO: Pasta 'cartas/' não encontrada. Usando fallback de retângulos.")
            return imagens

        # Verso da carta
        verso_path = os.path.join(pasta, "back.png")
        if os.path.exists(verso_path):
            img = pygame.image.load(verso_path)
            imagens["verso"] = pygame.transform.smoothscale(img, (LARGURA_CARTA, ALTURA_CARTA))

        # Mapeamento: valor → string, naipe → código
        valores_map = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
                       8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K"}
        naipes_map = {"copas": "H", "ouros": "D", "paus": "C", "espadas": "S"}  # H=Hearts, D=Diamonds, etc.

        carregadas = 0
        for naipe in ["copas", "ouros", "paus", "espadas"]:
            for valor in range(1, 14):
                val_str = valores_map[valor]
                naipe_codigo = naipes_map[naipe]
                nome_arq = f"{val_str}{naipe_codigo}.png"  # Ex: "AH.png"
                caminho = os.path.join(pasta, nome_arq)
                if os.path.exists(caminho):
                    chave = f"{valores_map[valor]} de {naipe}"
                    img = pygame.image.load(caminho)
                    imagens[chave] = pygame.transform.smoothscale(img, (LARGURA_CARTA, ALTURA_CARTA))
                    carregadas += 1

        print(f"Carregadas {carregadas} imagens de cartas (de 52).")
        return imagens

    # ------------------------------------------------------------------
    # MÉTODO: desenhar_carta
    # Desenha carta com imagem ou fallback
    # ------------------------------------------------------------------
    def desenhar_carta(self, carta, x, y, face_up=True, destaque=False):
        if face_up and carta:
            chave = str(carta)  # Ex: "A de copas"
            img = self.imagens_cartas.get(chave)
            if img:
                self.tela.blit(img, (x, y))
            else:
                # Fallback: retângulo com texto
                pygame.draw.rect(self.tela, BRANCO, (x, y, LARGURA_CARTA, ALTURA_CARTA))
                pygame.draw.rect(self.tela, PRETO, (x, y, LARGURA_CARTA, ALTURA_CARTA), 2)
                cor = VERMELHO if carta.is_vermelho() else PRETO
                texto = self.fonte_pequena.render(chave, True, cor)
                self.tela.blit(texto, (x + 5, y + 5))
        else:
            # Verso ou carta virada
            verso = self.imagens_cartas.get("verso")
            if verso:
                self.tela.blit(verso, (x, y))
            else:
                pygame.draw.rect(self.tela, (0, 0, 100), (x, y, LARGURA_CARTA, ALTURA_CARTA))
                pygame.draw.rect(self.tela, PRETO, (x, y, LARGURA_CARTA, ALTURA_CARTA), 2)

        # Destaque ao arrastar
        if destaque:
            s = pygame.Surface((LARGURA_CARTA, ALTURA_CARTA), pygame.SRCALPHA)
            s.fill(DESTAQUE)
            self.tela.blit(s, (x, y))

    # ------------------------------------------------------------------
    # MÉTODOS DE DESENHO
    # ------------------------------------------------------------------
    def desenhar_fundo(self):
        self.tela.fill(VERDE_MESA)
        # Linhas guia para colunas
        for i in range(7):
            x = MARGEM_ESQUERDA + i * ESPACO_HORIZONTAL
            pygame.draw.line(self.tela, (0, 80, 0), (x, MARGEM_TOPO - 40), (x, ALTURA_TELA - 50), 2)

    def desenhar_botao_novo_jogo(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicou = pygame.mouse.get_pressed()[0]
        dentro = (BOTAO_X <= mouse_x <= BOTAO_X + BOTAO_LARGURA and
                  BOTAO_Y <= mouse_y <= BOTAO_Y + BOTAO_ALTURA)

        cor_fundo = (0, 150, 0) if dentro else (0, 120, 0)
        pygame.draw.rect(self.tela, cor_fundo, (BOTAO_X, BOTAO_Y, BOTAO_LARGURA, BOTAO_ALTURA))
        pygame.draw.rect(self.tela, BRANCO, (BOTAO_X, BOTAO_Y, BOTAO_LARGURA, BOTAO_ALTURA), 3)

        texto = self.fonte.render("NOVO JOGO", True, BRANCO)
        texto_rect = texto.get_rect(center=(BOTAO_X + BOTAO_LARGURA//2, BOTAO_Y + BOTAO_ALTURA//2))
        self.tela.blit(texto, texto_rect)

        if dentro and clicou:
            self.jogo = JogoYukon()
            self.arrastando = False
            self.subpilha_arrastada = []

    def desenhar_titulo(self):
        titulo = self.fonte.render("PACIÊNCIA YUKON", True, BRANCO)
        self.tela.blit(titulo, (MARGEM_ESQUERDA, 80))

    def desenhar_tableau(self):
        for col_idx, pilha in enumerate(self.jogo.tableau):
            x = MARGEM_ESQUERDA + col_idx * ESPACO_HORIZONTAL
            for i, carta in enumerate(pilha.cartas):
                y = MARGEM_TOPO + i * SOBREPOSICAO
                destaque = (self.arrastando and self.origem_coluna == col_idx and i >= self.origem_indice)
                self.desenhar_carta(carta, x, y, carta.face_up, destaque)

    def desenhar_fundacoes(self):
        simbolos = ["(spades)", "(hearts)", "(diamonds)", "(clubs)"]
        for i, fund in enumerate(self.jogo.fundacoes):
            x = FUNDOES_X_INICIAL + i * 100
            y = FUNDOES_Y
            if fund.is_vazia():
                pygame.draw.rect(self.tela, BRANCO, (x, y, LARGURA_CARTA, ALTURA_CARTA), 3)
                texto = self.fonte.render(simbolos[i], True, BRANCO)
                self.tela.blit(texto, (x + 20, y + 40))
            else:
                self.desenhar_carta(fund.peek(), x, y, True)

    def desenhar_subpilha_arrastada(self, mouse_x, mouse_y):
        if not self.arrastando or not self.subpilha_arrastada:
            return
        x = mouse_x - self.offset_x
        y = mouse_y - self.offset_y
        for i, carta in enumerate(self.subpilha_arrastada):
            self.desenhar_carta(carta, x, y + i * SOBREPOSICAO, True, True)

    def desenhar_vitoria(self):
        if self.jogo.verificar_vitoria():
            vitoria = self.fonte_vitoria.render("VITÓRIA!", True, (255, 215, 0))
            fundo = pygame.Surface((400, 100), pygame.SRCALPHA)
            fundo.fill((0, 0, 0, 180))
            self.tela.blit(fundo, (LARGURA_TELA//2 - 200, ALTURA_TELA//2 - 50))
            self.tela.blit(vitoria, (LARGURA_TELA//2 - 120, ALTURA_TELA//2 - 40))

    # ------------------------------------------------------------------
    # INTERAÇÃO COM MOUSE
    # ------------------------------------------------------------------
    def coordenadas_para_coluna(self, x, y):
        # Tableau
        for col in range(7):
            col_x = MARGEM_ESQUERDA + col * ESPACO_HORIZONTAL
            if col_x <= x < col_x + LARGURA_CARTA:
                return ("tableau", col)
        # Fundações
        for i in range(4):
            fund_x = FUNDOES_X_INICIAL + i * 100
            if fund_x <= x < fund_x + LARGURA_CARTA and FUNDOES_Y <= y < FUNDOES_Y + ALTURA_CARTA:
                return ("fundacao", i)
        return (None, None)

    def encontrar_subpilha_clicada(self, x, y):
        for col_idx, pilha in enumerate(self.jogo.tableau):
            col_x = MARGEM_ESQUERDA + col_idx * ESPACO_HORIZONTAL
            for i, carta in enumerate(pilha.cartas):
                carta_y = MARGEM_TOPO + i * SOBREPOSICAO
                if (col_x <= x < col_x + LARGURA_CARTA and
                    carta_y <= y < carta_y + ALTURA_CARTA and
                    carta.face_up):
                    return col_idx, i
        return None, None

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = evento.pos
                # Evita clique no botão novo jogo
                if (BOTAO_X <= x <= BOTAO_X + BOTAO_LARGURA and
                    BOTAO_Y <= y <= BOTAO_Y + BOTAO_ALTURA):
                    continue

                col, idx = self.encontrar_subpilha_clicada(x, y)
                if col is not None:
                    pilha = self.jogo.tableau[col]
                    self.subpilha_arrastada = pilha.get_subpilha(idx)
                    self.origem_coluna = col
                    self.origem_indice = idx
                    self.offset_x = x - (MARGEM_ESQUERDA + col * ESPACO_HORIZONTAL)
                    self.offset_y = y - (MARGEM_TOPO + idx * SOBREPOSICAO)
                    self.arrastando = True

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and self.arrastando:
                x, y = evento.pos
                tipo, idx = self.coordenadas_para_coluna(x, y)
                sucesso = False
                if tipo == "tableau" and idx != self.origem_coluna:
                    sucesso = self.jogo.mover_subpilha(self.origem_coluna, self.origem_indice, idx)
                elif tipo == "fundacao" and len(self.subpilha_arrastada) == 1:
                    sucesso = self.jogo.mover_para_fundacao(self.origem_coluna)

                self.arrastando = False
                self.subpilha_arrastada = []

    # ------------------------------------------------------------------
    # LOOP PRINCIPAL
    # ------------------------------------------------------------------
    def rodar(self):
        while True:
            self.tratar_eventos()

            # Desenho
            self.desenhar_fundo()
            self.desenhar_botao_novo_jogo()
            self.desenhar_titulo()
            self.desenhar_tableau()
            self.desenhar_fundacoes()
            self.desenhar_vitoria()

            # Subpilha arrastada por cima
            if self.arrastando:
                mx, my = pygame.mouse.get_pos()
                self.desenhar_subpilha_arrastada(mx, my)

            pygame.display.flip()
            self.clock.tick(FPS)


# ===================================================================
# EXECUÇÃO
# ===================================================================
if __name__ == "__main__":
    app = InterfacePygame()
    app.rodar()