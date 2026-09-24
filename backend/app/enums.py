import enum

class TipoUsuario(str, enum.Enum):
    MORADOR = "morador"
    ADMIN = "admin"

class TipoCategoria(str, enum.Enum):
    ALAGAMENTO = "alagamento"
    ARVORE = "arvore"
    BUEIRO = "bueiro"
    BURACO = "buraco"
    ENTULHO = "entulho"
    POSTE = "poste"
    VAZAMENTO = "vazamento"
    OUTRO = "outro"

class TipoStatus(str, enum.Enum):
    CORRIGIDO = "corrigido"
    EM_ANDAMENTO = "em_andamento"
    PENDENTE = "pendente"