# src/game/jogo_yukon.py
# Esta é a classe principal do jogo Yukon
# Controla: baralho, tableau (7 colunas), fundações (4 pilhas), movimentos e vitória

from src.models.baralho import Baralho
from src.models.pilha import Pilha
from typing import List


class JogoYukon:
    # ------------------------------------------------------------------
    # CONSTRUTOR
    # Cria o jogo: 7 colunas no tableau, 4 fundações, baralho
    # ------------------------------------------------------------------
    def __init__(self):
        # 7 pilhas para as colunas do jogo (tableau)
        self.tableau: List[Pilha] = [Pilha() for _ in range(7)]
        
        # 4 pilhas para montar os naipes (fundações)
        self.fundacoes: List[Pilha] = [Pilha() for _ in range(4)]
        
        # O baralho com 52 cartas
        self.baralho = Baralho()
        
        # Monta o jogo com distribuição inicial
        self.setup()

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # MÉTODO: setup (100% CORRETO - Yukon oficial)
    # Total: 52 cartas
    # - Coluna 0: 1 face-up
    # - Colunas 1 a 6: N face-down + 5 face-up (N = índice da coluna)
    # Total face-up: 1 + 6×5 = 31
    # Total face-down: 1+2+3+4+5+6 = 21
    # Total: 31 + 21 = 52
    # ------------------------------------------------------------------
    def setup(self):
        self.baralho.embaralhar()

        # === DISTRIBUIÇÃO CORRETA ===
        # Para cada coluna (0 a 6)
        for col_idx in range(7):
            # Quantidade de face-down (0 para coluna 0, 1 para 1, etc.)
            face_down_count = col_idx  # 0,1,2,3,4,5,6

            # 1. Adiciona face-down
            for _ in range(face_down_count):
                carta = self.baralho.distribuir(1)[0]  # face-down
                self.tableau[col_idx].push(carta)

            # 2. Adiciona 5 face-up (todas as colunas têm 5 face-up, exceto coluna 0 que tem 1)
            face_up_count = 1 if col_idx == 0 else 5
            for _ in range(face_up_count):
                carta = self.baralho.distribuir(1)[0]
                carta.virar()  # face-up
                self.tableau[col_idx].push(carta)

        # Verificação final
        total = sum(p.tamanho() for p in self.tableau)
        if total != 52:
            raise RuntimeError(f"ERRO CRÍTICO: {total} cartas distribuídas (esperado 52)")

    # ------------------------------------------------------------------
    # MÉTODO: mover_subpilha
    # Move uma subpilha de uma coluna para outra
    # Parâmetros:
    # - origem_idx: índice da coluna de origem (0 a 6)
    # - inicio_subpilha: índice da carta inicial da subpilha (0 = fundo)
    # - destino_idx: índice da coluna de destino
    # Retorna True se moveu com sucesso
    # ------------------------------------------------------------------
    def mover_subpilha(self, origem_idx: int, inicio_subpilha: int, destino_idx: int) -> bool:
        origem = self.tableau[origem_idx]
        destino = self.tableau[destino_idx]

        # Validações básicas
        if origem_idx == destino_idx:
            return False
        if inicio_subpilha >= origem.tamanho():
            return False

        # Pega a subpilha a ser movida
        subpilha = origem.get_subpilha(inicio_subpilha)

        # Verifica se pode colocar no destino
        if not destino.pode_adicionar_subpilha(subpilha):
            return False

        # === MOVE ===
        origem.remover_subpilha(inicio_subpilha)
        destino.adicionar_subpilha(subpilha)
        
        # Se a carta do topo da origem estava virada para baixo, vira
        origem.virar_topo_se_necessario()
        
        return True

    # ------------------------------------------------------------------
    # MÉTODO: mover_para_fundacao
    # Move a carta do topo de uma coluna para a fundação correta
    # Só move se for a próxima carta do naipe (ex: 5 sobre 4 de mesmo naipe)
    # ------------------------------------------------------------------
    def mover_para_fundacao(self, coluna_idx: int) -> bool:
        origem = self.tableau[coluna_idx]
        carta = origem.peek()  # Carta do topo
        if not carta or not carta.face_up:
            return False

        # Procura a fundação correta (mesmo naipe)
        for fund in self.fundacoes:
            topo = fund.peek()
            # Pode colocar se:
            # - Fundação vazia e carta é Ás (valor 1)
            # - Ou carta é 1 acima do topo e mesmo naipe
            if (topo is None and carta.valor == 1) or \
               (topo and topo.naipe == carta.naipe and carta.valor == topo.valor + 1):
                # Move a carta
                fund.push(origem.pop())
                origem.virar_topo_se_necessario()
                return True
        return False

    # ------------------------------------------------------------------
    # MÉTODO: verificar_vitoria
    # Verifica se o jogo foi ganho (todas as 52 cartas nas fundações)
    # ------------------------------------------------------------------
    def verificar_vitoria(self) -> bool:
        # Cada fundação deve ter 13 cartas
        return all(fund.tamanho() == 13 for fund in self.fundacoes)

    # ------------------------------------------------------------------
    # MÉTODO: exibir_estado
    # Mostra o jogo no terminal (para debug)
    # ------------------------------------------------------------------
    def exibir_estado(self):
        print("\n" + "="*50)
        print("TABLEAU (7 colunas):")
        for i, pilha in enumerate(self.tableau):
            print(f"  Col {i}: {pilha}")
        print("\nFUNDAÇÕES (4 naipes):")
        for i, fund in enumerate(self.fundacoes):
            if fund.is_vazia():
                print(f"  Fund {i}: [vazia]")
            else:
                print(f"  Fund {i}: {fund}")
        print("="*50)