# teste.py
# Teste completo do Jogo Yukon

from src.game.jogo_yukon import JogoYukon

print("INICIANDO O JOGO YUKON...")
jogo = JogoYukon()
jogo.exibir_estado()

# Teste: mover uma carta de uma coluna para fundação (se for Ás)
print("\nTentando mover Ás para fundação...")
for i in range(7):
    if jogo.mover_para_fundacao(i):
        print(f"Ás movido da coluna {i}!")
        break

jogo.exibir_estado()

# Teste: mover subpilha (exemplo: da coluna 1, a partir da 2ª carta visível)
print("\nTentando mover subpilha da coluna 1 (índice 1) para coluna 0...")
sucesso = jogo.mover_subpilha(1, 1, 0)
print("Sucesso?" if sucesso else "Falhou", sucesso)

jogo.exibir_estado()