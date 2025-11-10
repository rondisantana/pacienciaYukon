# tests/test_pilha.py
# Testes unitários para a classe Pilha (Yukon)
# Verifica: push, pop, subpilhas, regras de movimento

import unittest
import sys
import os

# Adiciona o diretório src/ ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.pilha import Pilha
from src.models.carta import Carta, Naipe


class TestPilha(unittest.TestCase):

    def test_pilha_vazia(self):
        p = Pilha()
        self.assertTrue(p.is_vazia())
        self.assertEqual(p.tamanho(), 0)
        self.assertIsNone(p.peek())

    def test_push_pop_basico(self):
        p = Pilha()
        c1 = Carta(1, Naipe.COPAS)
        c2 = Carta(2, Naipe.PAUS)
        p.push(c1)
        p.push(c2)
        self.assertEqual(p.pop(), c2)
        self.assertEqual(p.pop(), c1)
        self.assertTrue(p.is_vazia())

    def test_get_subpilha(self):
        p = Pilha()
        k = Carta(13, Naipe.PAUS); k.virar()
        q = Carta(12, Naipe.COPAS); q.virar()
        j = Carta(11, Naipe.OUROS); j.virar()
        p.push(k); p.push(q); p.push(j)
        sub = p.get_subpilha(1)
        self.assertEqual(len(sub), 2)
        self.assertEqual(sub[0].valor, 12)
        self.assertEqual(sub[1].valor, 11)

    def test_pode_adicionar_subpilha_valida(self):
        p = Pilha()
        rei = Carta(13, Naipe.PAUS); rei.virar(); p.push(rei)
        dama = Carta(12, Naipe.COPAS); dama.virar()
        self.assertTrue(p.pode_adicionar_subpilha([dama]))

    def test_pode_adicionar_subpilha_invalida(self):
        p = Pilha()
        rei = Carta(13, Naipe.PAUS); rei.virar(); p.push(rei)
        valete = Carta(11, Naipe.OUROS); valete.virar()
        self.assertFalse(p.pode_adicionar_subpilha([valete]))

    def test_pilha_vazia_aceita_so_rei(self):
        p = Pilha()
        rei = Carta(13, Naipe.ESPADAS); rei.virar()
        dama = Carta(12, Naipe.COPAS); dama.virar()
        self.assertTrue(p.pode_adicionar_subpilha([rei]))
        self.assertFalse(p.pode_adicionar_subpilha([dama]))

    def test_virar_carta_apos_pop(self):
        p = Pilha()
        fundo = Carta(5, Naipe.PAUS)  # virada para baixo
        topo = Carta(6, Naipe.COPAS); topo.virar()
        p.push(fundo)
        p.push(topo)
        p.pop()
        self.assertTrue(fundo.face_up)  # Virou automaticamente


if __name__ == '__main__':
    unittest.main(verbosity=2)