# src/gui/interface_pygame.py
# Alunos: Rondineli, Jonas, Antônio e Frizzo
# PACIÊNCIA YUKON — ESTRUTURA DE DADOS II
# Silvia Brandão 2025

import pygame
import sys
import os
from src.game.jogo_yukon import JogoYukon

# ===================================================================
# CONFIGURAÇÕES GLOBAIS DO JOGO
# ===================================================================
LARGURA_TELA_PADRAO = 1200          # Largura padrão da janela
ALTURA_TELA_PADRAO = 800            # Altura padrão da janela
FPS = 60                            # Taxa de atualização (frames por segundo)

# Cores utilizadas na interface
VERDE_MESA = (0, 100, 0)            # Cor de fundo da mesa de jogo
BRANCO = (255, 255, 255)            # Cor branca (texto, bordas)
PRETO = (0, 0, 0)                   # Cor preta (contornos, texto)
VERMELHO = (220, 20, 60)            # Cor vermelha (naipe copas/ouros)
DESTAQUE_DICA = (255, 255, 100, 130)# Destaque amarelo translúcido para dicas
HOVER_BOTAO = (0, 180, 0)           # Cor do botão ao passar o mouse

# Dimensões das cartas
LARGURA_CARTA = 80                  # Largura de cada carta
ALTURA_CARTA = 116                  # Altura de cada carta
SOBREPOSICAO = 30                   # Sobreposição vertical entre cartas no tableau

# Configurações do painel lateral esquerdo
PAINEL_LARGURA = 180                # Largura do painel de controle
PAINEL_X = 20                       # Posição X do painel
PAINEL_Y = 20                       # Posição Y do painel
PAINEL_COR = (0, 80, 0)             # Cor de fundo do painel
PAINEL_BORDA = (200, 200, 200)      # Cor da borda do painel

# Posição do título "PACIÊNCIA YUKON"
TITULO_X = PAINEL_X + 20
TITULO_Y = PAINEL_Y + 20

# Configurações dos botões no painel
BOTAO_X = PAINEL_X + 20             # Posição X dos botões
BOTAO_Y = TITULO_Y + 70             # Posição Y inicial do primeiro botão
BOTAO_LARGURA = 140                 # Largura dos botões
BOTAO_ALTURA = 40                   # Altura dos botões
ESPACO_BOTOES = 15                  # Espaço entre os botões

# Posições específicas de cada botão
BOTAO_DICA_X = BOTAO_X
BOTAO_DICA_Y = BOTAO_Y
BOTAO_NOVO_X = BOTAO_X
BOTAO_NOVO_Y = BOTAO_DICA_Y + BOTAO_ALTURA + ESPACO_BOTOES
BOTAO_DESFAZER_X = BOTAO_X
BOTAO_DESFAZER_Y = BOTAO_NOVO_Y + BOTAO_ALTURA + ESPACO_BOTOES

# Configurações das fundações (pilhas de destino)
FUNDAÇÃO_X = PAINEL_X + 50          # Posição X das fundações
FUNDAÇÃO_Y_INICIAL = BOTAO_DESFAZER_Y + BOTAO_ALTURA + 50  # Y inicial da primeira fundação
FUNDAÇÃO_ESPACO_VERTICAL = 120      # Espaço vertical entre as fundações

# Configurações do cronômetro (canto inferior direito)
CRONOMETRO_LARGURA = 140
CRONOMETRO_ALTURA = 50
CRONOMETRO_MARGEM = 20

# Configurações do tableau (7 colunas principais)
TABLEAU_X_INICIAL = PAINEL_X + PAINEL_LARGURA + 20  # X inicial do tableau
TABLEAU_Y = 20                      # Y inicial do tableau

# ===================================================================
# CLASSE PRINCIPAL DA INTERFACE GRÁFICA
# ===================================================================
class InterfacePygame:
    def __init__(self):
        """
        Inicializa a interface gráfica do jogo Paciência Yukon.
        Configura a janela, fontes, imagens, estado do jogo e variáveis de controle.
        """
        pygame.init()
        pygame.display.set_caption("Paciência Yukon")

        # Controle de tela cheia
        self.tela_cheia = False
        self.largura_padrao = LARGURA_TELA_PADRAO
        self.altura_padrao = ALTURA_TELA_PADRAO
        self.tela = pygame.display.set_mode((self.largura_padrao, self.altura_padrao), pygame.RESIZABLE)

        # Controle de FPS
        self.clock = pygame.time.Clock()

        # Fontes utilizadas no jogo
        self.fonte = pygame.font.SysFont("Arial", 24, bold=True)        # Fonte principal
        self.fonte_pequena = pygame.font.SysFont("Arial", 18)           # Fonte para botões e detalhes
        self.fonte_vitoria = pygame.font.SysFont("Arial", 48, bold=True)# Fonte para mensagem de vitória

        # Carrega imagens das cartas
        self.imagens_cartas = self.carregar_imagens()
        self.jogo = JogoYukon()  # Instancia o jogo lógico

        # Estado do arrasto de cartas
        self.arrastando = False
        self.subpilha_arrastada = []
        self.origem_coluna = None
        self.origem_indice = None
        self.offset_x = 0
        self.offset_y = 0
        self.origem_tipo = None

        # Histórico para desfazer jogadas
        self.historico = [self.jogo.salvar_estado()]
        self.ultimo_desfazer = 0
        self.DEBOUNCE_TEMPO = 300  # Evita múltiplos cliques rápidos

        # Controle de duplo clique
        self.ultimo_clique_tempo = 0
        self.ultimo_clique_pos = (0, 0)
        self.DUPLO_CLIQUE_TEMPO = 300
        self.DUPLO_CLIQUE_DISTANCIA = 10

        # Cronômetro
        self.tempo_inicio = None
        self.tempo_total_ms = 0
        self.cronometro_ativo = False
        self.primeiro_clique_feito = False

        # Sistema de dicas
        self.dica_ativa = False
        self.cartas_destacadas = []

    def alternar_tela_cheia(self, forcar=None):
        """
        Alterna entre modo janela e tela cheia.
        Parâmetro 'forcar' permite forçar um estado específico.
        """
        if forcar is not None:
            self.tela_cheia = forcar
        else:
            self.tela_cheia = not self.tela_cheia
        if self.tela_cheia:
            self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.tela = pygame.display.set_mode((self.largura_padrao, self.altura_padrao), pygame.RESIZABLE)

    def carregar_imagens(self):
        """
        Carrega as imagens das cartas do diretório 'cartas'.
        Usa fallback se imagens não existirem.
        """
        imagens = {}
        raiz_projeto = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        pasta_cartas = os.path.join(raiz_projeto, "cartas")
        if not os.path.exists(pasta_cartas):
            return imagens

        # Carrega o verso da carta
        for verso_nome in ["back_dark.png", "back.png"]:
            verso_path = os.path.join(pasta_cartas, verso_nome)
            if os.path.exists(verso_path):
                img = pygame.image.load(verso_path)
                imagens["verso"] = pygame.transform.smoothscale(img, (LARGURA_CARTA, ALTURA_CARTA))
                break

        # Mapeamento de naipes e valores
        naipes_map = {"copas": "hearts", "ouros": "diamonds", "paus": "clubs", "espadas": "spades"}
        valores_map = {1: "A", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
                       8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K"}

        # Carrega cada carta individualmente
        for naipe_nome, prefixo in naipes_map.items():
            for valor, val_str in valores_map.items():
                nome_arq = f"{prefixo}_{val_str}.png"
                caminho = os.path.join(pasta_cartas, nome_arq)
                if os.path.exists(caminho):
                    chave = f"{val_str} de {naipe_nome}"
                    img = pygame.image.load(caminho)
                    imagens[chave] = pygame.transform.smoothscale(img, (LARGURA_CARTA, ALTURA_CARTA))

        return imagens

    def desenhar_carta(self, carta, x, y, face_up=True, destaque_dica=False):
        """
        Desenha uma carta na posição (x, y).
        Se face_up=False, mostra o verso.
        Se destaque_dica=True, aplica efeito de destaque.
        """
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
        if destaque_dica:
            s = pygame.Surface((LARGURA_CARTA, ALTURA_CARTA), pygame.SRCALPHA)
            s.fill(DESTAQUE_DICA)
            self.tela.blit(s, (x, y))

    def desenhar_fundo(self):
        """
        Desenha o fundo verde da mesa e o painel lateral esquerdo.
        Calcula dinamicamente a altura do painel para cobrir todas as fundações.
        """
        self.tela.fill(VERDE_MESA)
        largura_atual, altura_atual = self.tela.get_size()

        # Calcula a posição Y da última fundação
        ultima_fundacao_y = FUNDAÇÃO_Y_INICIAL + 3 * FUNDAÇÃO_ESPACO_VERTICAL
        # Define altura do painel com margem inferior
        painel_altura = ultima_fundacao_y + ALTURA_CARTA + 100

        # Garante que o painel não ultrapasse a tela
        painel_altura = min(painel_altura, altura_atual - 25)

        # Desenha o retângulo do painel com borda
        painel_rect = pygame.Rect(PAINEL_X, PAINEL_Y, PAINEL_LARGURA, painel_altura)
        pygame.draw.rect(self.tela, PAINEL_COR, painel_rect)
        pygame.draw.rect(self.tela, PAINEL_BORDA, painel_rect, 4)

    def desenhar_botao(self, texto, x, y, largura, altura, hover=False):
        """
        Desenha um botão com efeito hover.
        """
        cor_fundo = HOVER_BOTAO if hover else (0, 100, 0)
        pygame.draw.rect(self.tela, cor_fundo, (x, y, largura, altura), border_radius=10)
        pygame.draw.rect(self.tela, BRANCO, (x, y, largura, altura), 3, border_radius=10)
        txt = self.fonte_pequena.render(texto, True, BRANCO)
        txt_rect = txt.get_rect(center=(x + largura//2, y + altura//2))
        self.tela.blit(txt, txt_rect)

    def desenhar_botao_dica(self):
        """
        Desenha o botão "DICA" com destaque quando ativo.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dentro = (BOTAO_DICA_X <= mouse_x <= BOTAO_DICA_X + BOTAO_LARGURA and
                  BOTAO_DICA_Y <= mouse_y <= BOTAO_DICA_Y + BOTAO_ALTURA)
        cor_texto = (255, 255, 0) if self.dica_ativa else BRANCO
        self.desenhar_botao("DICA", BOTAO_DICA_X, BOTAO_DICA_Y, BOTAO_LARGURA, BOTAO_ALTURA, dentro)

    def desenhar_botao_novo_jogo(self):
        """
        Desenha o botão "NOVO JOGO".
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dentro = (BOTAO_NOVO_X <= mouse_x <= BOTAO_NOVO_X + BOTAO_LARGURA and
                  BOTAO_NOVO_Y <= mouse_y <= BOTAO_NOVO_Y + BOTAO_ALTURA)
        self.desenhar_botao("NOVO JOGO", BOTAO_NOVO_X, BOTAO_NOVO_Y, BOTAO_LARGURA, BOTAO_ALTURA, dentro)

    def desenhar_botao_desfazer(self):
        """
        Desenha o botão "DESFAZER" apenas se houver jogadas para desfazer.
        """
        if len(self.historico) <= 1:
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dentro = (BOTAO_DESFAZER_X <= mouse_x <= BOTAO_DESFAZER_X + BOTAO_LARGURA and
                  BOTAO_DESFAZER_Y <= mouse_y <= BOTAO_DESFAZER_Y + BOTAO_ALTURA)
        self.desenhar_botao("DESFAZER", BOTAO_DESFAZER_X, BOTAO_DESFAZER_Y, BOTAO_LARGURA, BOTAO_ALTURA, dentro)

    def desfazer_ultima_jogada(self):
        """
        Restaura o estado anterior do jogo.
        """
        if len(self.historico) > 1:
            self.historico.pop()
            self.jogo.restaurar_estado(self.historico[-1])
            self.dica_ativa = False
            self.cartas_destacadas = []

    def desenhar_titulo(self):
        """
        Desenha o título "PACIÊNCIA YUKON" no painel.
        """
        pac = self.fonte.render("PACIÊNCIA", True, BRANCO)
        yuk = self.fonte.render("YUKON", True, BRANCO)
        self.tela.blit(pac, (TITULO_X, TITULO_Y))
        self.tela.blit(yuk, (TITULO_X, TITULO_Y + 30))

    def desenhar_tableau(self):
        """
        Desenha as 7 colunas do tableau com cartas sobrepostas.
        Ajusta o espaçamento horizontal dinamicamente conforme o tamanho da tela.
        """
        largura_tela, _ = self.tela.get_size()
        espaco_disponivel = largura_tela - TABLEAU_X_INICIAL - 50
        espaco_horizontal = espaco_disponivel // 7

        for col_idx, pilha in enumerate(self.jogo.tableau):
            x = TABLEAU_X_INICIAL + col_idx * espaco_horizontal
            for i, carta in enumerate(pilha.cartas):
                y = TABLEAU_Y + i * SOBREPOSICAO
                destaque_arrasto = (self.arrastando and self.origem_coluna == col_idx and
                                  self.origem_tipo == "tableau" and i >= self.origem_indice)
                destaque_dica = False

                if self.dica_ativa:
                    for o, inicio, tam in self.cartas_destacadas:
                        if o == col_idx and inicio <= i < inicio + tam:
                            destaque_dica = True
                            break

                self.desenhar_carta(carta, x, y, carta.face_up, destaque_dica or destaque_arrasto)

    def desenhar_fundacoes_vertical(self):
        """
        Desenha as 4 fundações verticais no painel esquerdo.
        Mostra ícones dos naipes quando vazias e a carta do topo quando ocupadas.
        """
        for i, fund in enumerate(self.jogo.fundacoes):
            x = FUNDAÇÃO_X
            y = FUNDAÇÃO_Y_INICIAL + i * FUNDAÇÃO_ESPACO_VERTICAL
            rect = pygame.Rect(x, y, LARGURA_CARTA, ALTURA_CARTA)
            pygame.draw.rect(self.tela, (0, 60, 0), rect, border_radius=12)
            pygame.draw.rect(self.tela, BRANCO, rect, 3, border_radius=12)
            if fund.is_vazia():
                # Fonte pequena para caber
                fonte = pygame.font.SysFont("Segoe UI Symbol", 16)
                cor = (200, 200, 200)
                
                # Linha superior: ♠ ♥
                linha1 = fonte.render("♠  ♥", True, cor)
                linha1_rect = linha1.get_rect(centerx=rect.centerx, y=y + 30)
                self.tela.blit(linha1, linha1_rect)
                
                # Linha inferior: ♦ ♣
                linha2 = fonte.render("♦  ♣", True, cor)
                linha2_rect = linha2.get_rect(centerx=rect.centerx, y=y + 55)
                self.tela.blit(linha2, linha2_rect)
            else:
                destaque = self.dica_ativa and any(o == -1 and inc == i for o, inc, _ in self.cartas_destacadas)
                self.desenhar_carta(fund.peek(), x, y, True, destaque)

    def coordenadas_para_coluna(self, x, y):
        """
        Converte coordenadas do mouse em (tipo, índice) de coluna ou fundação.
        """
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

    def encontrar_subpilha_clicada(self, mx, my):
        """
        Encontra a subpilha clicada no tableau com base nas coordenadas do mouse.
        """
        largura_tela, _ = self.tela.get_size()
        espaco_disponivel = largura_tela - TABLEAU_X_INICIAL - 50
        espaco_horizontal = espaco_disponivel // 7
        for col_idx, pilha in enumerate(self.jogo.tableau):
            x = TABLEAU_X_INICIAL + col_idx * espaco_horizontal
            if x <= mx < x + LARGURA_CARTA:
                y_inicial = TABLEAU_Y
                for idx, carta in enumerate(pilha.cartas):
                    y_topo = y_inicial + idx * SOBREPOSICAO
                    y_limite = y_topo + ALTURA_CARTA if idx == len(pilha.cartas) - 1 else y_inicial + (idx + 1) * SOBREPOSICAO
                    if y_topo <= my < y_limite and carta.face_up:
                        return col_idx, idx
        return None

    def calcular_dicas_completas(self):
        """
        Calcula todas as jogadas válidas possíveis para o sistema de dicas.
        """
        self.cartas_destacadas = []

        # TABLEAU → TABLEAU
        for origem in range(7):
            pilha = self.jogo.tableau[origem]
            if not pilha.cartas:
                continue

            for inicio in range(len(pilha.cartas)):
                if not pilha.cartas[inicio].face_up:
                    continue

                subpilha = [pilha.cartas[inicio]]
                for i in range(inicio + 1, len(pilha.cartas)):
                    proxima = pilha.cartas[i]
                    anterior = subpilha[-1]
                    if (proxima.valor == anterior.valor - 1 and
                        proxima.is_vermelho() != anterior.is_vermelho()):
                        subpilha.append(proxima)
                    else:
                        break

                if len(subpilha) >= 1:
                    for destino in range(7):
                        if origem == destino:
                            continue
                        if self.jogo.tableau[destino].pode_adicionar_subpilha(subpilha):
                            self.cartas_destacadas.append((origem, inicio, len(subpilha)))
                            break

        # TABLEAU → FUNDAÇÃO
        for col in range(7):
            pilha = self.jogo.tableau[col]
            if pilha.cartas and pilha.cartas[-1].face_up:
                carta = pilha.cartas[-1]
                for fund_idx in range(4):
                    if self.jogo.pode_mover_para_fundacao(carta, fund_idx):
                        self.cartas_destacadas.append((col, len(pilha.cartas)-1, 1))
                        break

        # FUNDAÇÃO → TABLEAU
        for fund_idx in range(4):
            fund = self.jogo.fundacoes[fund_idx]
            if fund.is_vazia():
                continue
            carta = fund.peek()
            for col in range(7):
                if self.jogo.tableau[col].pode_adicionar_subpilha([carta]):
                    self.cartas_destacadas.append((-1, fund_idx, 1))
                    break

    def tratar_eventos(self):
        """
        Processa todos os eventos do Pygame (mouse, teclado, janela).
        """
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

                # Botão DICA
                if (BOTAO_DICA_X <= x <= BOTAO_DICA_X + BOTAO_LARGURA and
                    BOTAO_DICA_Y <= y <= BOTAO_DICA_Y + BOTAO_ALTURA):
                    self.dica_ativa = not self.dica_ativa
                    if self.dica_ativa:
                        self.calcular_dicas_completas()
                    else:
                        self.cartas_destacadas = []
                    continue

                # Botão NOVO JOGO
                if (BOTAO_NOVO_X <= x <= BOTAO_NOVO_X + BOTAO_LARGURA and
                    BOTAO_NOVO_Y <= y <= BOTAO_NOVO_Y + BOTAO_ALTURA):
                    self.jogo = JogoYukon()
                    self.historico = [self.jogo.salvar_estado()]
                    self.dica_ativa = False
                    self.cartas_destacadas = []
                    self.primeiro_clique_feito = False
                    self.cronometro_ativo = False
                    self.tempo_total_ms = 0
                    continue

                # Botão DESFAZER
                if (len(self.historico) > 1 and
                    BOTAO_DESFAZER_X <= x <= BOTAO_DESFAZER_X + BOTAO_LARGURA and
                    BOTAO_DESFAZER_Y <= y <= BOTAO_DESFAZER_Y + BOTAO_ALTURA and
                    agora - self.ultimo_desfazer > self.DEBOUNCE_TEMPO):
                    self.desfazer_ultima_jogada()
                    self.ultimo_desfazer = agora
                    continue

                # Duplo clique
                tempo_desde_ultimo = agora - self.ultimo_clique_tempo
                dist_x = abs(x - self.ultimo_clique_pos[0])
                dist_y = abs(y - self.ultimo_clique_pos[1])
                if (tempo_desde_ultimo < self.DUPLO_CLIQUE_TEMPO and
                    dist_x < self.DUPLO_CLIQUE_DISTANCIA and
                    dist_y < self.DUPLO_CLIQUE_DISTANCIA):
                    self.tentar_mover_duplo_clique(x, y)
                    self.ultimo_clique_tempo = 0
                    continue
                self.ultimo_clique_tempo = agora
                self.ultimo_clique_pos = (x, y)

                if not self.primeiro_clique_feito:
                    self.iniciar_cronometro()

                # Início do arrasto no tableau
                resultado = self.encontrar_subpilha_clicada(x, y)
                if resultado is not None:
                    col, idx = resultado
                    pilha = self.jogo.tableau[col]
                    subpilha = [pilha.cartas[idx]]
                    for i in range(idx + 1, len(pilha.cartas)):
                        proxima = pilha.cartas[i]
                        anterior = subpilha[-1]
                        if (proxima.valor == anterior.valor - 1 and
                            proxima.is_vermelho() != anterior.is_vermelho()):
                            subpilha.append(proxima)
                        else:
                            break
                    self.subpilha_arrastada = subpilha
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
                    # Início do arrasto na fundação
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
                # Fim do arrasto
                if self.arrastando:
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
                        if self.dica_ativa:
                            self.calcular_dicas_completas()
                    self.arrastando = False
                    self.subpilha_arrastada = []
                    self.origem_coluna = None
                    self.origem_indice = None
                    self.origem_tipo = None

    def iniciar_cronometro(self):
        """
        Inicia o cronômetro na primeira interação do usuário.
        """
        if not self.primeiro_clique_feito:
            self.tempo_inicio = pygame.time.get_ticks()
            self.cronometro_ativo = True
            self.primeiro_clique_feito = True

    def tentar_mover_duplo_clique(self, mx, my):
        """
        Tenta mover automaticamente a carta do topo para uma fundação ao dar duplo clique.
        """
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
        for fund_idx in range(4):
            if self.jogo.pode_mover_para_fundacao(carta, fund_idx):
                if self.jogo.mover_para_fundacao(col, fund_idx):
                    self.historico.append(self.jogo.salvar_estado())
                    if self.dica_ativa:
                        self.calcular_dicas_completas()
                    return

    def formatar_tempo(self, ms):
        """
        Converte milissegundos em formato MM:SS.
        """
        minutos = ms // 60000
        segundos = (ms % 60000) // 1000
        return f"{minutos:02d}:{segundos:02d}"

    def desenhar_cronometro(self):
        """
        Desenha o cronômetro no canto inferior direito.
        """
        largura, altura = self.tela.get_size()
        x = largura - CRONOMETRO_LARGURA - CRONOMETRO_MARGEM
        y = altura - CRONOMETRO_ALTURA - CRONOMETRO_MARGEM

        tempo_atual = self.tempo_total_ms
        if self.cronometro_ativo and self.tempo_inicio is not None:
            tempo_atual += (pygame.time.get_ticks() - self.tempo_inicio)

        texto = self.fonte.render(self.formatar_tempo(tempo_atual), True, BRANCO)
        texto_rect = texto.get_rect(center=(x + CRONOMETRO_LARGURA // 2, y + CRONOMETRO_ALTURA // 2))

        fundo = pygame.Surface((CRONOMETRO_LARGURA, CRONOMETRO_ALTURA), pygame.SRCALPHA)
        fundo.fill((0, 80, 0, 240))
        self.tela.blit(fundo, (x, y))
        pygame.draw.rect(self.tela, BRANCO, (x, y, CRONOMETRO_LARGURA, CRONOMETRO_ALTURA), 3, border_radius=10)
        self.tela.blit(texto, texto_rect)

    def rodar(self):
        """
        Loop principal do jogo.
        Processa eventos, atualiza e desenha a tela a cada frame.
        """
        while True:
            self.tratar_eventos()

            largura_atual, altura_atual = self.tela.get_size()
            if not self.tela_cheia and (largura_atual != self.largura_padrao or altura_atual != self.altura_padrao):
                self.largura_padrao = largura_atual
                self.altura_padrao = altura_atual

            if self.jogo.verificar_vitoria() and self.cronometro_ativo:
                self.tempo_total_ms += pygame.time.get_ticks() - self.tempo_inicio
                self.cronometro_ativo = False

            self.desenhar_fundo()
            self.desenhar_titulo()
            self.desenhar_botao_dica()
            self.desenhar_botao_novo_jogo()
            self.desenhar_botao_desfazer()
            self.desenhar_fundacoes_vertical()
            self.desenhar_tableau()
            self.desenhar_cronometro()
            self.desenhar_vitoria()

            if self.arrastando:
                mx, my = pygame.mouse.get_pos()
                self.desenhar_subpilha_arrastada(mx, my)

            pygame.display.flip()
            self.clock.tick(FPS)

    def desenhar_subpilha_arrastada(self, mouse_x, mouse_y):
        """
        Desenha a subpilha sendo arrastada com o mouse.
        """
        if not self.arrastando or not self.subpilha_arrastada:
            return
        x = mouse_x - self.offset_x
        y = mouse_y - self.offset_y
        for i, carta in enumerate(self.subpilha_arrastada):
            self.desenhar_carta(carta, x, y + i * SOBREPOSICAO, True, True)

    def desenhar_vitoria(self):
        """
        Exibe mensagem de vitória ao completar o jogo.
        """
        if self.jogo.verificar_vitoria():
            vitoria = self.fonte_vitoria.render("VITÓRIA!", True, (255, 215, 0))
            fundo = pygame.Surface((400, 100), pygame.SRCALPHA)
            fundo.fill((0, 0, 0, 180))
            largura_tela, altura_tela = self.tela.get_size()
            self.tela.blit(fundo, (largura_tela//2 - 200, altura_tela//2 - 50))
            self.tela.blit(vitoria, (largura_tela//2 - 120, altura_tela//2 - 40))

    def desenhar_fallback(self, carta, x, y):
        """
        Desenha uma carta alternativa (texto) caso a imagem não exista.
        """
        pygame.draw.rect(self.tela, BRANCO, (x, y, LARGURA_CARTA, ALTURA_CARTA))
        pygame.draw.rect(self.tela, PRETO, (x, y, LARGURA_CARTA, ALTURA_CARTA), 2)
        cor = VERMELHO if carta.is_vermelho() else PRETO
        texto = self.fonte_pequena.render(str(carta), True, cor)
        self.tela.blit(texto, (x + 5, y + 5))

    def desenhar_fallback_verso(self, x, y):
        """
        Desenha o verso da carta caso a imagem não exista.
        """
        pygame.draw.rect(self.tela, (0, 0, 100), (x, y, LARGURA_CARTA, ALTURA_CARTA))
        pygame.draw.rect(self.tela, PRETO, (x, y, LARGURA_CARTA, ALTURA_CARTA), 2)

# ===================================================================
if __name__ == "__main__":
    app = InterfacePygame()
    app.rodar()