# src/models/baralho.py
# Esta classe representa o baralho completo com 52 cartas
# Responsável por: criar, embaralhar e distribuir as cartas

import random  # Para embaralhar as cartas
from typing import List
from src.models.carta import Carta, Naipe  # Importa Carta e Naipe


class Baralho:
    # ------------------------------------------------------------------
    # CONSTRUTOR
    # Cria um baralho com 52 cartas (4 naipes × 13 valores)
    # ------------------------------------------------------------------
    def __init__(self):
        self.cartas: List[Carta] = []  # Lista que vai guardar todas as 52 cartas
        self._criar_baralho()          # Chama o método que monta o baralho

    # ------------------------------------------------------------------
    # MÉTODO PRIVADO: _criar_baralho
    # Cria todas as 52 cartas e coloca na lista
    # É privado (começa com _) porque só é usado dentro da classe
    # ------------------------------------------------------------------
    def _criar_baralho(self):
        # Para cada naipe (copas, ouros, paus, espadas)
        for naipe in [Naipe.COPAS, Naipe.OUROS, Naipe.PAUS, Naipe.ESPADAS]:
            # Para cada valor de 1 a 13 (Ás até Rei)
            for valor in range(1, 14):
                # Cria a carta e adiciona na lista
                carta = Carta(valor, naipe)
                self.cartas.append(carta)

    # ------------------------------------------------------------------
    # MÉTODO: embaralhar
    # Embaralha as cartas de forma aleatória
    # Usa o algoritmo Fisher-Yates (padrão do Python)
    # ------------------------------------------------------------------
    def embaralhar(self):
        random.shuffle(self.cartas)  # Embaralha a lista no local

    # ------------------------------------------------------------------
    # MÉTODO: distribuir
    # Remove e retorna as primeiras 'quantidade' cartas do baralho
    # Ex: distribuir(5) → retorna 5 cartas do topo
    # ------------------------------------------------------------------
    def distribuir(self, quantidade: int) -> List[Carta]:
        if quantidade > len(self.cartas):
            raise ValueError("Não há cartas suficientes no baralho")
        
        # Pega as primeiras 'quantidade' cartas
        cartas_distribuidas = self.cartas[:quantidade]
        # Remove elas do baralho
        self.cartas = self.cartas[quantidade:]
        # Retorna as cartas distribuídas
        return cartas_distribuidas

    # ------------------------------------------------------------------
    # MÉTODO ESPECIAL: __len__
    # Permite usar len(baralho) para saber quantas cartas restam
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self.cartas)

    # ------------------------------------------------------------------
    # MÉTODO ESPECIAL: __str__
    # Mostra o baralho (útil para debug)
    # Mostra só as primeiras 10 cartas para não poluir
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        if not self.cartas:
            return "Baralho vazio"
        amostra = self.cartas[:10]
        return "Baralho: " + ", ".join(str(c) for c in amostra) + ("..." if len(self.cartas) > 10 else "")