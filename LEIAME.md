# Paciência Yukon — Estrutura de Dados II

**Alunos:** Rondineli, Jonas, Antônio e Frizzo
**Professora:** Silvia Brandão  
**Semestre:** 2025.2

================================================================================

## Visão Geral

Jogo de **Paciência Yukon** desenvolvido em **Python** com a biblioteca **Pygame**.  
Implementa a lógica completa do jogo, interface gráfica responsiva, sistema de dicas, desfazer jogada, cronômetro, tela cheia e atalho na área de trabalho.

================================================================================

## Principais Classes

### `Carta` (`src/models/carta.py`)

Representa uma carta do baralho.

- **Atributos**: `valor` (1 = Ás … 13 = Rei), `naipe`, `face_up`.
- **Métodos**:
  - `is_vermelho()` → `True` se o naipe for **copas** ou **ouros**.
  - `__str__()` → ex.: `"A de copas"`.

---

### `Pilha` (`src/models/pilha.py`)

Estrutura de pilha para **tableau** e **fundação**.

- **Tableau**:
  - Permite mover **qualquer subpilha contígua de cartas viradas para cima**.
  - A subpilha **não precisa estar ordenada** para ser movida.
  - Só pode ser colocada em coluna com **carta do topo de valor imediatamente superior e cor oposta**.
- **Fundação**:
  - Aceita **apenas cartas do mesmo naipe** em ordem **crescente**, começando pelo Ás.

---

### `JogoYukon` (`src/game/jogo_yukon.py`)

Gerencia toda a lógica do jogo.

- **Principais métodos**:
  - `iniciar_jogo()` – embaralha e distribui as 52 cartas.
  - `mover_subpilha(origem, início, destino)` – move qualquer subpilha contígua válida.
  - `mover_para_fundacao(coluna, fund_idx)` – move carta do tableau para fundação.
  - `pode_mover_para_fundacao(carta, fund_idx)` – valida movimento.
  - `verificar_vitoria()` – retorna `True` quando todas as fundações estão completas.

---

### `InterfacePygame` (`src/gui/interface_pygame.py`)

Responsável pela interface gráfica.

- **Funcionalidades**:
  - Painel lateral com botões **DICA**, **NOVO JOGO** e **DESFAZER**.
  - Fundações verticais exibindo **4 naipes em formato 2×2** quando vazias.
  - **Cronômetro** no canto inferior direito (inicia no primeiro clique).
  - Sistema de **dica** que destaca jogadas válidas.
  - **Desfazer** com histórico completo.
  - **Duplo clique** move carta automaticamente para a fundação.
  - Janela redimensionável + **tela cheia (F11)**.

================================================================================

## Regras do Jogo (Yukon) – Explicação Detalhada

### **Objetivo**

Construir as 4 fundações em ordem **crescente** (Ás → 2 → … → Rei), **uma para cada naipe**.

================================================================================

### **Distribuição Inicial**

- **7 colunas (tableau)** com **52 cartas** no total.
- **Apenas a primeira coluna tem 1 carta virada para cima.**
- **As colunas 2 a 7 têm 5 cartas viradas para cima cada.**

| Coluna | Cartas totais | Viradas para baixo | Viradas para cima |
| ------ | ------------- | ------------------ | ----------------- |
| 1      | 1             | 0                  | **1**             |
| 2      | 6             | 1                  | **5**             |
| 3      | 7             | 2                  | **5**             |
| 4      | 8             | 3                  | **5**             |
| 5      | 9             | 4                  | **5**             |
| 6      | 10            | 5                  | **5**             |
| 7      | 11            | 6                  | **5**             |

**Resumo**:

- **28 cartas viradas para baixo** (0 + 1 + 2 + 3 + 4 + 5 + 6)
- **24 cartas viradas para cima** (1 + 5×5)
- **Nenhuma carta sobrando** (não há monte de compra)

================================================================================

### **Movimentação**

- **No tableau**:

  - Pode mover **qualquer sequência contígua de cartas viradas para cima** (não precisa estar ordenada).
  - A subpilha pode ser colocada em outra coluna **somente se**:
    - A carta do topo da coluna de destino for de **valor imediatamente superior** à **primeira carta da subpilha**.
    - E tiver **cor oposta** (vermelho/preto).
  - Exemplo: Pode mover `7 de copas` + `6 de ouros` + `10 de paus` como bloco, mesmo que não esteja em sequência de ordenação correta.

- **Para fundação**:

  - Apenas **uma carta por vez**.
  - Deve ser do **mesmo naipe** e **valor imediatamente superior** à carta do topo da fundação.

- **Virar carta**:
  - Ao mover uma subpilha, a carta abaixo é automaticamente virada para cima.

================================================================================

### **Condições de Vitória**

Todas as 52 cartas estão nas 4 fundações, ordenadas de **Ás a Rei** por naipe.

================================================================================

## Como Executar

### **Opção 1 – Pelo terminal (recomendado para desenvolvimento)**

```bash
cd caminho/para/PACIENCIAYUKON
python main.py
```

### **Opção 2 - Criando atalho na área de trabalho**

1 - Execute uma única vez:

```bash
python criar_atalho.py
```

Um atalho “Paciência Yukon” será criado na sua Área de Trabalho.

================================================================================

## Requisitos e Instalação

O único pacote externo necessário é o Pygame:
pygame==2.6.1

Instale com:

```bash
pip install -r requirements.txt
```

Requisito: Python 3.11+ instalado.
