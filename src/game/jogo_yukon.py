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
        for col_idx in range(7):
            face_down_count = col_idx  # 0,1,2,3,4,5,6

            # 1. Adiciona face-down
            for _ in range(face_down_count):
                carta = self.baralho.distribuir(1)[0]
                self.tableau[col_idx].push(carta)

            # 2. Adiciona face-up
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
    # ------------------------------------------------------------------
    def mover_subpilha(self, origem_idx: int, inicio_subpilha: int, destino_idx: int) -> bool:
        origem = self.tableau[origem_idx]
        destino = self.tableau[destino_idx]

        if origem_idx == destino_idx or inicio_subpilha >= origem.tamanho():
            return False

        subpilha = origem.get_subpilha(inicio_subpilha)
        if not destino.pode_adicionar_subpilha(subpilha):
            return False

        origem.remover_subpilha(inicio_subpilha)
        destino.adicionar_subpilha(subpilha)
        origem.virar_topo_se_necessario()
        return True

    # ------------------------------------------------------------------
    # MÉTODO: mover_para_fundacao
    # Move a carta do topo de uma coluna para uma fundação específica
    # ------------------------------------------------------------------
    def mover_para_fundacao(self, coluna_idx: int, fund_idx: int) -> bool:
        origem = self.tableau[coluna_idx]
        carta = origem.peek()
        if not carta or not carta.face_up:
            return False

        fund = self.fundacoes[fund_idx]
        topo = fund.peek()

        # Pode colocar se:
        # - Fundação vazia e carta é Ás
        # - Ou carta é 1 acima do topo e mesmo naipe
        if (topo is None and carta.valor == 1) or \
           (topo and topo.naipe == carta.naipe and carta.valor == topo.valor + 1):
            fund.push(origem.pop())
            origem.virar_topo_se_necessario()
            return True
        return False

    # ------------------------------------------------------------------
    # MÉTODO: pode_mover_para_fundacao (NOVO - PARA DUPLO CLIQUE)
    # Verifica se uma carta pode ser movida para uma fundação específica
    # ------------------------------------------------------------------
    def pode_mover_para_fundacao(self, carta, fund_idx: int) -> bool:
        """Verifica se a carta pode ser movida para a fundação específica."""
        if carta is None:
            return False
        fund = self.fundacoes[fund_idx]
        topo = fund.peek()
        if topo is None:
            return carta.valor == 1  # só Ás
        else:
            return (carta.naipe == topo.naipe and
                    carta.valor == topo.valor + 1)

    # ------------------------------------------------------------------
    # MÉTODO: mover_da_fundacao
    # Move a carta do topo de uma fundação para uma coluna do tableau
    # ------------------------------------------------------------------
    def mover_da_fundacao(self, fund_idx: int, destino_idx: int) -> bool:
        fund = self.fundacoes[fund_idx]
        if fund.is_vazia():
            return False
        
        carta = fund.peek()
        destino = self.tableau[destino_idx]
        
        if destino.pode_adicionar_subpilha([carta]):
            destino.adicionar_subpilha([fund.pop()])
            return True
        return False

    # ------------------------------------------------------------------
    # MÉTODO: verificar_vitoria
    # ------------------------------------------------------------------
    def verificar_vitoria(self) -> bool:
        return all(fund.tamanho() == 13 for fund in self.fundacoes)

    # ------------------------------------------------------------------
    # MÉTODO: exibir_estado (debug)
    # ------------------------------------------------------------------
    def exibir_estado(self):
        print("\n" + "="*50)
        print("TABLEAU (7 colunas):")
        for i, pilha in enumerate(self.tableau):
            print(f"  Col {i}: {pilha}")
        print("\nFUNDAÇÕES (4 naipes):")
        for i, fund in enumerate(self.fundacoes):
            print(f"  Fund {i}: {fund}" if not fund.is_vazia() else f"  Fund {i}: [vazia]")
        print("="*50)

    # ------------------------------------------------------------------
    # MÉTODOS DE DESFAZER
    # ------------------------------------------------------------------
    def salvar_estado(self):
        """Retorna uma cópia profunda do estado atual do jogo."""
        return {
            'tableau': [pilha.cartas[:] for pilha in self.tableau],
            'fundacoes': [pilha.cartas[:] for pilha in self.fundacoes],
        }

    def restaurar_estado(self, estado):
        """Restaura o estado do jogo a partir de um snapshot."""
        # Limpa e restaura tableau
        for i, pilha in enumerate(self.tableau):
            pilha.cartas = estado['tableau'][i][:]

        # Limpa e restaura fundações
        for i, pilha in enumerate(self.fundacoes):
            pilha.cartas = estado['fundacoes'][i][:]