# src/models/carta.py
# Este arquivo define as classes "Naipe" e "Carta"
# São as peças básicas do jogo de paciência

# ----------------------------------------------------------------------
# CLASSE: Naipe
# Representa os 4 naipes do baralho: copas, ouros, paus, espadas
# Usamos uma classe simples (sem herança de Enum) para facilitar o entendimento
# ----------------------------------------------------------------------
class Naipe:
    # Definindo os 4 naipes como "constantes" da classe
    # Cada um é uma string com o nome do naipe
    COPAS = "copas"       # Naipe vermelho
    OUROS = "ouros"       # Naipe vermelho
    PAUS = "paus"         # Naipe preto
    ESPADAS = "espadas"   # Naipe preto

    # ------------------------------------------------------------------
    # MÉTODO ESTÁTICO: is_vermelho
    # Verifica se um naipe é vermelho (copas ou ouros)
    # @staticmethod significa que não precisa de um objeto para usar
    # ------------------------------------------------------------------
    @staticmethod
    def is_vermelho(naipe):
        # Verifica se o naipe está na lista de naipes vermelhos
        return naipe in [Naipe.COPAS, Naipe.OUROS]

    # ------------------------------------------------------------------
    # MÉTODO ESTÁTICO: is_preto
    # Verifica se um naipe é preto (paus ou espadas)
    # ------------------------------------------------------------------
    @staticmethod
    def is_preto(naipe):
        # Verifica se o naipe está na lista de naipes pretos
        return naipe in [Naipe.PAUS, Naipe.ESPADAS]


# ----------------------------------------------------------------------
# CLASSE: Carta
# Representa uma única carta do baralho
# Exemplo: Ás de copas, 7 de paus, Rei de espadas
# ----------------------------------------------------------------------
class Carta:
    # Dicionário que converte números em nomes especiais
    # 1 = Ás, 11 = Valete, 12 = Dama, 13 = Rei
    # Outros números (2 a 10) ficam como estão
    VALORES = {1: "A", 11: "J", 12: "Q", 13: "K"}

    # ------------------------------------------------------------------
    # MÉTODO CONSTRUTOR: __init__
    # É chamado quando você faz: carta = Carta(1, Naipe.COPAS)
    # ------------------------------------------------------------------
    def __init__(self, valor: int, naipe: str):
        # Verifica se o valor está entre 1 e 13
        if valor not in range(1, 14):
            # Se não estiver, dá erro com mensagem clara
            raise ValueError("Valor deve ser de 1 a 13")
        
        # Salva o valor da carta (1 = Ás, 13 = Rei)
        self.valor = valor
        
        # Salva o naipe da carta (ex: "copas")
        self.naipe = naipe
        
        # Define se a carta está virada para cima ou para baixo
        # False = virada para baixo (não visível no jogo)
        self.face_up = False

    # ------------------------------------------------------------------
    # MÉTODO: virar
    # Vira a carta para cima (mostra o valor e naipe)
    # ------------------------------------------------------------------
    def virar(self):
        self.face_up = True  # Agora a carta está visível

    # ------------------------------------------------------------------
    # MÉTODO: is_vermelho
    # Verifica se ESTA carta é vermelha
    # Usa o método da classe Naipe
    # ------------------------------------------------------------------
    def is_vermelho(self):
        return Naipe.is_vermelho(self.naipe)

    # ------------------------------------------------------------------
    # MÉTODO: is_preto
    # Verifica se ESTA carta é preta
    # ------------------------------------------------------------------
    def is_preto(self):
        return Naipe.is_preto(self.naipe)

    # ------------------------------------------------------------------
    # MÉTODO ESPECIAL: __str__
    # Define como a carta será mostrada quando usamos print(carta)
    # Exemplo: "A de copas"
    # ------------------------------------------------------------------
    def __str__(self):
        # Pega o nome do valor (A, J, Q, K) ou o número normal
        valor_str = self.VALORES.get(self.valor, str(self.valor))
        # Junta o valor + " de " + naipe
        return f"{valor_str} de {self.naipe}"