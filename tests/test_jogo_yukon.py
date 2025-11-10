# tests/test_jogo_yukon.py
# Testes unitários para JogoYukon - CORRIGIDO
# Força Ás virado e usa Naipe corretamente

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.game.jogo_yukon import JogoYukon
from src.models.carta import Carta, Naipe
from src.models.pilha import Pilha


class TestJogoYukon(unittest.TestCase):

    def setUp(self):
        self.jogo = JogoYukon()

    def test_setup_distribui_52_cartas(self):
        total = sum(p.tamanho() for p in self.jogo.tableau) + sum(f.tamanho() for f in self.jogo.fundacoes)
        self.assertEqual(total, 52)

    def test_mover_para_fundacao_valido(self):
        # Força um Ás virado na coluna 0
        self.jogo.tableau[0].cartas.clear()
        as_copas = Carta(1, Naipe.COPAS)
        as_copas.virar()
        self.jogo.tableau[0].push(as_copas)

        sucesso = self.jogo.mover_para_fundacao(0)
        self.assertTrue(sucesso)
        self.assertEqual(self.jogo.fundacoes[0].tamanho(), 1)

    def test_mover_subpilha_valido(self):
        # Limpa colunas e força: Rei (preto) na coluna 0, Dama (vermelha) na coluna 1
        self.jogo.tableau[0].cartas.clear()
        self.jogo.tableau[1].cartas.clear()

        rei_paus = Carta(13, Naipe.PAUS); rei_paus.virar()
        dama_copas = Carta(12, Naipe.COPAS); dama_copas.virar()

        self.jogo.tableau[0].push(rei_paus)
        self.jogo.tableau[1].push(dama_copas)

        sucesso = self.jogo.mover_subpilha(1, 0, 0)  # Dama → sobre Rei
        self.assertTrue(sucesso)
        self.assertEqual(self.jogo.tableau[0].tamanho(), 2)
        self.assertEqual(self.jogo.tableau[1].tamanho(), 0)

    def test_mover_subpilha_invalido(self):
        # Força: Rei na 0, Valete (mesma cor) na 1
        self.jogo.tableau[0].cartas.clear()
        self.jogo.tableau[1].cartas.clear()

        rei_paus = Carta(13, Naipe.PAUS); rei_paus.virar()
        valete_paus = Carta(11, Naipe.PAUS); valete_paus.virar()

        self.jogo.tableau[0].push(rei_paus)
        self.jogo.tableau[1].push(valete_paus)

        sucesso = self.jogo.mover_subpilha(1, 0, 0)
        self.assertFalse(sucesso)

    def test_verificar_vitoria(self):
        # Cria fundações completas manualmente
        naipes = [Naipe.COPAS, Naipe.OUROS, Naipe.PAUS, Naipe.ESPADAS]
        for i, naipe in enumerate(naipes):
            pilha = Pilha()
            for valor in range(1, 14):
                carta = Carta(valor, naipe)
                carta.virar()
                pilha.push(carta)
            self.jogo.fundacoes[i] = pilha

        self.assertTrue(self.jogo.verificar_vitoria())


if __name__ == '__main__':
    unittest.main(verbosity=2)