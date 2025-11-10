# src/models/pilha.py
# Esta classe representa uma pilha de cartas (como uma coluna no jogo)
# Usamos lista do Python para simular uma pilha: o FINAL da lista é o TOPO

from typing import List, Optional
from src.models.carta import Carta  # Importa a classe Carta que criamos antes


class Pilha:
    # ------------------------------------------------------------------
    # CONSTRUTOR
    # Cria uma pilha vazia
    # ------------------------------------------------------------------
    def __init__(self):
        # Lista que armazena as cartas
        # Índice 0 = fundo da pilha
        # Último índice = topo da pilha (carta visível)
        self.cartas: List[Carta] = []

    # ------------------------------------------------------------------
    # MÉTODO: push
    # Adiciona uma carta no topo da pilha
    # ------------------------------------------------------------------
    def push(self, carta: Carta):
        self.cartas.append(carta)  # Adiciona no final da lista = topo

    # ------------------------------------------------------------------
    # MÉTODO: pop
    # Remove e retorna a carta do topo
    # Se a pilha estiver vazia, retorna None
    # ------------------------------------------------------------------
    def pop(self) -> Optional[Carta]:
        if not self.cartas:  # Se vazia
            return None
        
        carta_removida = self.cartas.pop()
        
        # Regra do Yukon: se ainda houver cartas, vira a do topo
        if self.cartas:
            self.cartas[-1].virar()  # Vira para cima
        
        return carta_removida

    # ------------------------------------------------------------------
    # MÉTODO: peek
    # Mostra a carta do topo SEM remover
    # Útil para verificar qual carta está visível
    # ------------------------------------------------------------------
    def peek(self) -> Optional[Carta]:
        if self.cartas:
            return self.cartas[-1]  # Última carta = topo
        return None

    # ------------------------------------------------------------------
    # MÉTODO: is_vazia
    # Verifica se a pilha não tem cartas
    # ------------------------------------------------------------------
    def is_vazia(self) -> bool:
        return len(self.cartas) == 0

    # ------------------------------------------------------------------
    # MÉTODO: tamanho
    # Retorna quantas cartas tem na pilha
    # ------------------------------------------------------------------
    def tamanho(self) -> int:
        return len(self.cartas)

    # ------------------------------------------------------------------
    # MÉTODO: get_subpilha
    # Pega uma parte da pilha a partir de um índice
    # Ex: get_subpilha(3) retorna as cartas do índice 3 até o topo
    # Isso é usado para mover várias cartas de uma vez (como no Yukon)
    # ------------------------------------------------------------------
    def get_subpilha(self, inicio: int) -> List[Carta]:
        return self.cartas[inicio:]  # Do índice 'inicio' até o final

    # ------------------------------------------------------------------
    # MÉTODO: pode_adicionar_subpilha
    # Verifica se pode colocar uma subpilha (várias cartas) sobre esta pilha
    # Regras do Yukon:
    # - Se a pilha estiver vazia → só aceita Rei (valor 13)
    # - Se não → a primeira carta da subpilha deve ser 1 menor e cor alternada
    # ------------------------------------------------------------------
    def pode_adicionar_subpilha(self, subpilha: List[Carta]) -> bool:
        if not subpilha:  # Subpilha vazia?
            return False

        carta_base = subpilha[0]  # Primeira carta da subpilha (a que vai encostar)

        if self.is_vazia():
            # Coluna vazia → só aceita Rei
            return carta_base.valor == 13
        else:
            # Pega a carta do topo atual
            topo_atual = self.peek()
            # Verifica: 1 menor + cor diferente
            return (carta_base.valor == topo_atual.valor - 1 and
                    carta_base.is_vermelho() != topo_atual.is_vermelho())

    # ------------------------------------------------------------------
    # MÉTODO: adicionar_subpilha
    # Adiciona várias cartas de uma vez no topo
    # ------------------------------------------------------------------
    def adicionar_subpilha(self, subpilha: List[Carta]):
        self.cartas.extend(subpilha)  # Junta as listas

    # ------------------------------------------------------------------
    # MÉTODO: remover_subpilha
    # Remove uma subpilha a partir de um índice e retorna ela
    # ------------------------------------------------------------------
    def remover_subpilha(self, inicio: int):
        subpilha = self.cartas[inicio:]   # Pega do índice até o final
        self.cartas = self.cartas[:inicio] # Remove da pilha original
        return subpilha

    # ------------------------------------------------------------------
    # MÉTODO: virar_topo_se_necessario
    # Depois de remover uma carta, se a nova carta do topo estiver virada para baixo,
    # vira ela para cima automaticamente
    # ------------------------------------------------------------------
    def virar_topo_se_necessario(self):
        if self.cartas and not self.cartas[-1].face_up:
            self.cartas[-1].virar()  # Vira a nova carta do topo

    # ------------------------------------------------------------------
    # MÉTODO ESPECIAL: __str__
    # Mostra a pilha como string para debug
    # Ex: "XX | XX | 5 de copas | K de paus"
    # XX = carta virada para baixo
    # ------------------------------------------------------------------
    def __str__(self):
        # Para cada carta: se face_up → mostra, senão → "XX"
        partes = []
        for carta in self.cartas:
            if carta.face_up:
                partes.append(str(carta))
            else:
                partes.append("XX")
        return " | ".join(partes)