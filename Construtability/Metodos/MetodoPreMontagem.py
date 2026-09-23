from enum import Enum

class MetodoPreMontagem(Enum):
    PRE_MONTAGEM_1 = 1 # Hub e nacele pré-montados
    PRE_MONTAGEM_2 = 2 # Metodo 1 + torre montada
    PRE_MONTAGEM_3 = 3 # 3 pas montadas no hub, a nacele é montada separadamente (Rotor estrela)
    PRE_MONTAGEM_4 = 4 # 2 pas + hub + nacele pré-montados (Orelha de coelho)
    PRE_MONTAGEM_5 = 5 # Metodo 4 + torre montada
    PRE_MONTAGEM_6 = 6 # Todos os itens montados

