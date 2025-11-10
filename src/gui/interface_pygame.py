# src/gui/interface_pygame.py
# JANELA NORMAL + F11 + ESC + DUPLO CLIQUE + DESFAZER + CRONÔMETRO + SEM ERROS

import pygame
import sys
import os
from src.game.jogo_yukon import JogoYukon

# ===================================================================
# CONFIGURAÇÕES
# ===================================================================
LARGURA_TELA_PADRAO = 1200
ALTURA_TELA_PADRAO = 800
FPS = 60

# Cores
VERDE_MESA = (0, 100, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (220, 20, 60)
DESTAQUE = (255, 255, 0, 80)

# Cartas
LARGURA_CARTA = 80
ALTURA_CARTA = 116
SOBREPOSICAO = 30

# PAINEL
PAINEL_LARGURA = 180
PAINEL_X = 20
PAINEL_Y = 20
PAINEL_COR = (0, 80, 0)
PAINEL_BORDA = (200, 200, 200)

# Título
TITULO_X = PAINEL_X + 20
TITULO_Y = PAINEL_Y + 20

# Botões
BOTAO_X = PAINEL_X + 20
BOTAO_Y = TITULO_Y + 80
BOTAO_LARGURA = 140
BOTAO_ALTURA = 40

BOTAO_DESFAZER_X = BOTAO_X
BOTAO_DESFAZER_Y = BOTAO_Y + BOTAO_ALTURA + 15
BOTAO_DESFAZER_LARGURA = 140
BOTAO_DESFAZER_ALTURA = 40

# Fundações
FUNDAÇÃO_X = PAINEL_X + 50
FUNDAÇÃO_Y_INICIAL = BOTAO_DESFAZER_Y + BOTAO_DESFAZER_ALTURA + 30
FUNDAÇÃO_ESPACO_VERTICAL = 130

# Tableau
TABLEAU_X_INICIAL = PAINEL_X + PAINEL_LARGURA + 20
TABLEAU_Y = 20

# ===================================================================
# CLASSE
# ===================================================================
class InterfacePygame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Paciência Yukon - Silvia Brandão 2025.2")

        # === CONTROLE DE TELA ===
        self.tela_cheia = False
        self.largura_padrao = LARGURA_TELA_PADRAO
        self.altura_padrao = ALTURA_TELA_PADRAO

        # ABRIR EM JANELA NORMAL
        self.tela = pygame.display.set_mode((self.largura_padrao, self.altura_padrao), pygame.RESIZABLE)

        self.clock = pygame.time.Clock()

        self.fonte = pygame.font.SysFont("Arial", 24, bold=True)
        self.fonte_pequena = pygame.font.SysFont("Arial", 18)
        self.fonte_vitoria = pygame.font.SysFont("Arial", 48, bold=True)

        self.imagens_cartas = self.carregar_imagens()
        self.jogo = JogoYukon()

        self.arrastando = False
        self.subpilha_arrastada = []
        self.origem_coluna = None
        self.origem_indice = None
        self.offset_x = 0
        self.offset_y = 0
        self.origem_tipo = None

        self.historico = [self.jogo.salvar_estado()]
        self.botao_desfazer_clicado = False

        self.ultimo_desfazer = 0
        self.DEBOUNCE_TEMPO = 300

        # === DUPLO CLIQUE ===
        self.ultimo_clique_tempo = 0
        self.ultimo_clique_pos = (0, 0)
        self.DUPLO_CLIQUE_TEMPO = 300
        self.DUPLO_CLIQUE_DISTANCIA = 10

        # === CRONÔMETRO ===
        self.tempo_inicio = None
        self.tempo_total_ms = 0
        self.cronometro_ativo = False

    # ------------------------------------------------------------------
    def alternar_tela_cheia(self, forcar=None):
        if forcar is not None:
            self.tela_cheia = forcar
        else:
            self.tela_cheia = not self.tela_cheia

        if self.tela_cheia:
            self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.tela = pygame.display.set_mode((self.largura_padrao, self.altura_padrao), pygame.RESIZABLE)

    # ------------------------------------------------------------------
    def carregar_imagens(self):
        imagens = {}
        raiz_projeto = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        pasta_cartas = os.path.join(raiz_projeto, "cartas")
        
        if not os.path.exists(pasta_cartas):
            return imagens

        for verso_nome in ["back_dark.png", "back.png"]:
            verso_path = os.path.join(pasta_cartas, verso_nome)
            if os.path.exists(verso_path):
                img = pygame.image.load(verso_path)
                imagens["verso"] = pygame.transform.smoothscale(img, (LARGURA_CARTA, ALTURA_CARTA))
                break

        naipes_map = {"copas": "hearts", "ouros": "diamonds", "paus": "clubs", "espadas": "spades"}
        valores_map = {1: "A", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
                       8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K"}

        for naipe_nome, prefixo in naipes_map.items():
            for valor, val_str in valores_map.items():
                nome_arq = f"{prefixo}_{val_str}.png"
                caminho = os.path.join(pasta_cartas, nome_arq)
                if os.path.exists(caminho):
                    chave = f"{val_str} de {naipe_nome}"
                    img = pygame.image.load(caminho)
                    imagens[chave] = pygame.transform.smoothscale(img, (LARGURA_CARTA, ALTURA_CARTA))

        return imagens

    # ------------------------------------------------------------------
    def desenhar_carta(self, carta, x, y, face_up=True, destaque=False):
        if face_up and carta:
            chave = str(carta)
            img = self.imagens_cartas.get(chave)
            if img:
                self.tela.blit(img, (x, y))
            else:
                self.desenhar_fallback(carta, x, y)
        else:
            verso = self.imagens_cartas.get("verso")
            if verso:
                self.tela.blit(verso, (x, y))
            else:
                self.desenhar_fallback_verso(x, y)

        if destaque:
            s = pygame.Surface((LARGURA_CARTA, ALTURA_CARTA), pygame.SRCALPHA)
            s.fill(DESTAQUE)
            self.tela.blit(s, (x, y))

    # ------------------------------------------------------------------
    def desenhar_fundo(self):
        self.tela.fill(VERDE_MESA)
        largura_atual, altura_atual = self.tela.get_size()
        painel_altura = altura_atual - 40
        painel_rect = pygame.Rect(20, 20, PAINEL_LARGURA, painel_altura)
        pygame.draw.rect(self.tela, PAINEL_COR, painel_rect)
        pygame.draw.rect(self.tela, PAINEL_BORDA, painel_rect, 4)

    # ------------------------------------------------------------------
    def desenhar_botao_novo_jogo(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dentro = (BOTAO_X <= mouse_x <= BOTAO_X + BOTAO_LARGURA and
                  BOTAO_Y <= mouse_y <= BOTAO_Y + BOTAO_ALTURA)
        cor_fundo = (0, 140, 0) if dentro else (0, 100, 0)
        pygame.draw.rect(self.tela, cor_fundo, (BOTAO_X, BOTAO_Y, BOTAO_LARGURA, BOTAO_ALTURA), border_radius=10)
        pygame.draw.rect(self.tela, BRANCO, (BOTAO_X, BOTAO_Y, BOTAO_LARGURA, BOTAO_ALTURA), 3, border_radius=10)

        texto = self.fonte_pequena.render("NOVO JOGO", True, BRANCO)
        texto_rect = texto.get_rect(center=(BOTAO_X + BOTAO_LARGURA//2, BOTAO_Y + BOTAO_ALTURA//2))
        self.tela.blit(texto, texto_rect)

    # ------------------------------------------------------------------
    def desenhar_botao_desfazer(self):
        if len(self.historico) <= 1:
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dentro = (BOTAO_DESFAZER_X <= mouse_x <= BOTAO_DESFAZER_X + BOTAO_DESFAZER_LARGURA and
                  BOTAO_DESFAZER_Y <= mouse_y <= BOTAO_DESFAZER_Y + BOTAO_DESFAZER_ALTURA)
        cor_fundo = (0, 140, 0) if dentro else (0, 100, 0)
        pygame.draw.rect(self.tela, cor_fundo, (BOTAO_DESFAZER_X, BOTAO_DESFAZER_Y, BOTAO_DESFAZER_LARGURA, BOTAO_DESFAZER_ALTURA), border_radius=10)
        pygame.draw.rect(self.tela, BRANCO, (BOTAO_DESFAZER_X, BOTAO_DESFAZER_Y, BOTAO_DESFAZER_LARGURA, BOTAO_DESFAZER_ALTURA), 3, border_radius=10)

        texto = self.fonte_pequena.render("DESFAZER", True, BRANCO)
        texto_rect = texto.get_rect(center=(BOTAO_DESFAZER_X + BOTAO_DESFAZER_LARGURA//2, BOTAO_DESFAZER_Y + BOTAO_DESFAZER_ALTURA//2))
        self.tela.blit(texto, texto_rect)

    # ------------------------------------------------------------------
    def desfazer_ultima_jogada(self):
        if len(self.historico) > 1:
            self.historico.pop()
            self.jogo.restaurar_estado(self.historico[-1])

    # ------------------------------------------------------------------
    def desenhar_titulo(self):
        pac = self.fonte.render("PACIÊNCIA", True, BRANCO)
        yuk = self.fonte.render("YUKON", True, BRANCO)
        self.tela.blit(pac, (TITULO_X, TITULO_Y))
        self.tela.blit(yuk, (TITULO_X, TITULO_Y + 30))

    # ------------------------------------------------------------------
    def desenhar_tableau(self):
        largura_tela, _ = self.tela.get_size()
        espaco_disponivel = largura_tela - TABLEAU_X_INICIAL - 50
        espaco_horizontal = espaco_disponivel // 7

        for col_idx, pilha in enumerate(self.jogo.tableau):
            x = TABLEAU_X_INICIAL + col_idx * espaco_horizontal
            for i, carta in enumerate(pilha.cartas):
                y = TABLEAU_Y + i * SOBREPOSICAO
                destaque = (self.arrastando and 
                           self.origem_coluna == col_idx and 
                           self.origem_tipo == "tableau" and
                           i >= self.origem_indice)
                self.desenhar_carta(carta, x, y, carta.face_up, destaque)

    # ------------------------------------------------------------------
    def desenhar_fundacoes_vertical(self):
        simbolos = ["spades", "hearts", "diamonds", "clubs"]
        for i, fund in enumerate(self.jogo.fundacoes):
            x = FUNDAÇÃO_X
            y = FUNDAÇÃO_Y_INICIAL + i * FUNDAÇÃO_ESPACO_VERTICAL
            rect = pygame.Rect(x, y, LARGURA_CARTA, ALTURA_CARTA)
            pygame.draw.rect(self.tela, (0, 60, 0), rect, border_radius=12)
            pygame.draw.rect(self.tela, BRANCO, rect, 3, border_radius=12)

            if fund.is_vazia():
                texto = self.fonte_pequena.render(simbolos[i], True, (200, 200, 200))
                texto_rect = texto.get_rect(center=rect.center)
                self.tela.blit(texto, texto_rect)
            else:
                self.desenhar_carta(fund.peek(), x, y, True)

    # ------------------------------------------------------------------
    def desenhar_subpilha_arrastada(self, mouse_x, mouse_y):
        if not self.arrastando or not self.subpilha_arrastada:
            return
        x = mouse_x - self.offset_x
        y = mouse_y - self.offset_y
        for i, carta in enumerate(self.subpilha_arrastada):
            self.desenhar_carta(carta, x, y + i * SOBREPOSICAO, True, True)

    # ------------------------------------------------------------------
    def desenhar_vitoria(self):
        if self.jogo.verificar_vitoria():
            vitoria = self.fonte_vitoria.render("VITÓRIA!", True, (255, 215, 0))
            fundo = pygame.Surface((400, 100), pygame.SRCALPHA)
            fundo.fill((0, 0, 0, 180))
            largura_tela, altura_tela = self.tela.get_size()
            self.tela.blit(fundo, (largura_tela//2 - 200, altura_tela//2 - 50))
            self.tela.blit(vitoria, (largura_tela//2 - 120, altura_tela//2 - 40))

    # ------------------------------------------------------------------
    def coordenadas_para_coluna(self, x, y):
        largura_tela, _ = self.tela.get_size()
        espaco_disponivel = largura_tela - TABLEAU_X_INICIAL - 50
        espaco_horizontal = espaco_disponivel // 7

        for i in range(4):
            fx = FUNDAÇÃO_X
            fy = FUNDAÇÃO_Y_INICIAL + i * FUNDAÇÃO_ESPACO_VERTICAL
            if fx <= x < fx + LARGURA_CARTA and fy <= y < fy + ALTURA_CARTA:
                return ("fundacao", i)
        for col in range(7):
            tx = TABLEAU_X_INICIAL + col * espaco_horizontal
            if tx <= x < tx + LARGURA_CARTA and TABLEAU_Y <= y < self.tela.get_height():
                return ("tableau", col)
        return (None, None)

    # ------------------------------------------------------------------
    def encontrar_subpilha_clicada(self, mx, my):
        largura_tela, _ = self.tela.get_size()
        espaco_disponivel = largura_tela - TABLEAU_X_INICIAL - 50
        espaco_horizontal = espaco_disponivel // 7

        for i, pilha in enumerate(self.jogo.tableau):
            x = TABLEAU_X_INICIAL + i * espaco_horizontal
            if x <= mx < x + LARGURA_CARTA:
                y_inicial = TABLEAU_Y
                for idx, carta in enumerate(pilha.cartas):
                    y_topo = y_inicial + idx * SOBREPOSICAO
                    y_limite = y_topo + ALTURA_CARTA if idx == len(pilha.cartas) - 1 else y_inicial + (idx + 1) * SOBREPOSICAO
                    if y_topo <= my < y_limite and carta.face_up:
                        return i, idx
        return None

    # ------------------------------------------------------------------
    def tentar_mover_duplo_clique(self, mx, my):
        resultado = self.encontrar_subpilha_clicada(mx, my)
        if resultado is None:
            return
        col, idx = resultado
        pilha = self.jogo.tableau[col]
        if idx != len(pilha.cartas) - 1:
            return
        carta = pilha.cartas[-1]
        if not carta.face_up:
            return

        for fund_idx, fund in enumerate(self.jogo.fundacoes):
            if self.jogo.pode_mover_para_fundacao(carta, fund_idx):
                if self.jogo.mover_para_fundacao(col, fund_idx):
                    self.historico.append(self.jogo.salvar_estado())
                    return

    # ------------------------------------------------------------------
    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_F11:
                    self.alternar_tela_cheia()
                elif evento.key == pygame.K_ESCAPE and self.tela_cheia:
                    self.alternar_tela_cheia(False)

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = evento.pos
                agora = pygame.time.get_ticks()

                # === DETECTAR DUPLO CLIQUE ===
                tempo_desde_ultimo = agora - self.ultimo_clique_tempo
                dist_x = abs(x - self.ultimo_clique_pos[0])
                dist_y = abs(y - self.ultimo_clique_pos[1])

                if (tempo_desde_ultimo < self.DUPLO_CLIQUE_TEMPO and
                    dist_x < self.DUPLO_CLIQUE_DISTANCIA and
                    dist_y < self.DUPLO_CLIQUE_DISTANCIA):
                    
                    self.tentar_mover_duplo_clique(x, y)
                    self.ultimo_clique_tempo = 0
                    continue

                # Atualizar último clique
                self.ultimo_clique_tempo = agora
                self.ultimo_clique_pos = (x, y)

                # === CLIQUE ÚNICO ===
                if (BOTAO_X <= x <= BOTAO_X + BOTAO_LARGURA and
                    BOTAO_Y <= y <= BOTAO_Y + BOTAO_ALTURA):
                    # === REINICIAR CRONÔMETRO AO CRIAR NOVO JOGO ===
                    self.tempo_inicio = pygame.time.get_ticks()
                    self.tempo_total_ms = 0
                    self.cronometro_ativo = True

                    self.jogo = JogoYukon()
                    self.historico = [self.jogo.salvar_estado()]
                    self.arrastando = False
                    self.subpilha_arrastada = []

                elif (BOTAO_DESFAZER_X <= x <= BOTAO_DESFAZER_X + BOTAO_DESFAZER_LARGURA and
                      BOTAO_DESFAZER_Y <= y <= BOTAO_DESFAZER_Y + BOTAO_DESFAZER_ALTURA and
                      len(self.historico) > 1 and
                      agora - self.ultimo_desfazer > self.DEBOUNCE_TEMPO):
                    self.botao_desfazer_clicado = True
                    self.ultimo_desfazer = agora

                else:
                    resultado = self.encontrar_subpilha_clicada(x, y)
                    if resultado is not None:
                        col, idx = resultado
                        pilha = self.jogo.tableau[col]
                        self.subpilha_arrastada = pilha.get_subpilha(idx)
                        self.origem_coluna = col
                        self.origem_indice = idx
                        self.origem_tipo = "tableau"
                        largura_tela, _ = self.tela.get_size()
                        espaco_disponivel = largura_tela - TABLEAU_X_INICIAL - 50
                        espaco_horizontal = espaco_disponivel // 7
                        self.offset_x = x - (TABLEAU_X_INICIAL + col * espaco_horizontal)
                        self.offset_y = y - (TABLEAU_Y + idx * SOBREPOSICAO)
                        self.arrastando = True
                    else:
                        tipo, idx = self.coordenadas_para_coluna(x, y)
                        if tipo == "fundacao":
                            fund = self.jogo.fundacoes[idx]
                            if not fund.is_vazia():
                                carta = fund.peek()
                                self.subpilha_arrastada = [carta]
                                self.origem_coluna = idx
                                self.origem_indice = 0
                                self.origem_tipo = "fundacao"
                                fund_y = FUNDAÇÃO_Y_INICIAL + idx * FUNDAÇÃO_ESPACO_VERTICAL
                                self.offset_x = x - FUNDAÇÃO_X
                                self.offset_y = y - fund_y
                                self.arrastando = True

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if self.botao_desfazer_clicado:
                    self.desfazer_ultima_jogada()
                    self.botao_desfazer_clicado = False

                elif self.arrastando:
                    x, y = evento.pos
                    tipo_destino, idx_destino = self.coordenadas_para_coluna(x, y)

                    movimento_valido = False

                    if (tipo_destino == "tableau" and self.origem_tipo == "tableau" and idx_destino != self.origem_coluna):
                        if self.jogo.mover_subpilha(self.origem_coluna, self.origem_indice, idx_destino):
                            movimento_valido = True
                    elif (tipo_destino == "fundacao" and self.origem_tipo == "tableau" and len(self.subpilha_arrastada) == 1):
                        if self.jogo.mover_para_fundacao(self.origem_coluna, idx_destino):
                            movimento_valido = True
                    elif (tipo_destino == "tableau" and self.origem_tipo == "fundacao"):
                        if self.jogo.mover_da_fundacao(self.origem_coluna, idx_destino):
                            movimento_valido = True

                    if movimento_valido:
                        self.historico.append(self.jogo.salvar_estado())

                    self.arrastando = False
                    self.subpilha_arrastada = []
                    self.origem_coluna = None
                    self.origem_indice = None
                    self.origem_tipo = None

    # ------------------------------------------------------------------
    def formatar_tempo(self, ms):
        """Formata milissegundos em MM:SS"""
        minutos = ms // 60000
        segundos = (ms % 60000) // 1000
        return f"{minutos:02d}:{segundos:02d}"

    # ------------------------------------------------------------------
    def desenhar_cronometro(self):
        """Desenha apenas o tempo (MM:SS) abaixo das fundações"""
        ultima_fund_y = FUNDAÇÃO_Y_INICIAL + 3 * FUNDAÇÃO_ESPACO_VERTICAL
        y_cronometro = ultima_fund_y + ALTURA_CARTA + 20
        x_cronometro = FUNDAÇÃO_X

        if self.cronometro_ativo:
            tempo_atual = self.tempo_total_ms + (pygame.time.get_ticks() - self.tempo_inicio)
        else:
            tempo_atual = self.tempo_total_ms

        texto_crono = self.fonte.render(self.formatar_tempo(tempo_atual), True, (255, 255, 255))
        texto_rect = texto_crono.get_rect(center=(x_cronometro + LARGURA_CARTA // 2, y_cronometro))

        fundo = pygame.Surface((LARGURA_CARTA + 20, 40), pygame.SRCALPHA)
        fundo.fill((0, 80, 0, 200))
        self.tela.blit(fundo, (x_cronometro - 10, y_cronometro - 15))
        self.tela.blit(texto_crono, texto_rect)

    # ------------------------------------------------------------------
    def rodar(self):
        while True:
            self.tratar_eventos()

            # === AJUSTAR REDIMENSIONAMENTO DA JANELA ===
            largura_atual, altura_atual = self.tela.get_size()
            if not self.tela_cheia and (largura_atual != self.largura_padrao or altura_atual != self.altura_padrao):
                self.largura_padrao = largura_atual
                self.altura_padrao = altura_atual

            # === PARAR CRONÔMETRO NA VITÓRIA ===
            if self.jogo.verificar_vitoria() and self.cronometro_ativo:
                self.tempo_total_ms += pygame.time.get_ticks() - self.tempo_inicio
                self.cronometro_ativo = False

            # === DESENHAR TUDO ===
            self.desenhar_fundo()
            self.desenhar_titulo()
            self.desenhar_botao_novo_jogo()
            self.desenhar_botao_desfazer()
            self.desenhar_cronometro()
            self.desenhar_fundacoes_vertical()
            self.desenhar_tableau()
            self.desenhar_vitoria()

            if self.arrastando:
                mx, my = pygame.mouse.get_pos()
                self.desenhar_subpilha_arrastada(mx, my)

            pygame.display.flip()
            self.clock.tick(FPS)

    # ------------------------------------------------------------------
    def desenhar_fallback(self, carta, x, y):
        pygame.draw.rect(self.tela, BRANCO, (x, y, LARGURA_CARTA, ALTURA_CARTA))
        pygame.draw.rect(self.tela, PRETO, (x, y, LARGURA_CARTA, ALTURA_CARTA), 2)
        cor = VERMELHO if carta.is_vermelho() else PRETO
        texto = self.fonte_pequena.render(str(carta), True, cor)
        self.tela.blit(texto, (x + 5, y + 5))

    def desenhar_fallback_verso(self, x, y):
        pygame.draw.rect(self.tela, (0, 0, 100), (x, y, LARGURA_CARTA, ALTURA_CARTA))
        pygame.draw.rect(self.tela, PRETO, (x, y, LARGURA_CARTA, ALTURA_CARTA), 2)

# ===================================================================
if __name__ == "__main__":
    app = InterfacePygame()
    app.rodar()