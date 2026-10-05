class SalaDeAula:
    """Representa uma sala de aula. Faz parte da Escola (Composição)."""

    def __init__(self, numero: str, capacidade: int):
        self.id = None
        self.numero = numero
        self.capacidade = capacidade

    def tem_vagas(self, qtd_alunos: int = 0) -> bool:
        if qtd_alunos < 0:
            return False
        return qtd_alunos < self.capacidade

    def to_dict(self):
        return {"id": self.id, "numero": self.numero, "capacidade": self.capacidade}


class Professor:
    """Representa um professor. Existe independentemente da Escola (Associação)."""

    def __init__(self, nome: str, disciplina: str):
        self.id = None
        self.nome = nome
        self.disciplina = disciplina
        self.escolas_ids = []

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "disciplina": self.disciplina,
            "escolas_ids": self.escolas_ids,
        }


class Escola:
    """Representa uma escola. É responsável por criar suas salas (Composição)."""

    def __init__(self, nome: str, cnpj: str):
        self.id = None
        self.nome = nome
        self.cnpj = cnpj
        self.salas: list[SalaDeAula] = []
        self.professores_ids: list[int] = []

    def adicionar_sala(self, numero: str, capacidade: int) -> SalaDeAula:
        sala = SalaDeAula(numero, capacidade)
        self.salas.append(sala)
        return sala

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "salas": [s.to_dict() for s in self.salas],
            "professores_ids": self.professores_ids,
        }


class Endereco:
    """Representa um endereço. Pode existir independentemente do Aluno (Agregação)."""

    def __init__(self, rua: str, numero: str, cidade: str, cep: str):
        self.id = None
        self.rua = rua
        self.numero = numero
        self.cidade = cidade
        self.cep = cep

    def endereco_formatado(self) -> str:
        return f"{self.rua}, {self.numero} - {self.cidade}, CEP: {self.cep}"

    def to_dict(self):
        return {
            "id": self.id,
            "rua": self.rua,
            "numero": self.numero,
            "cidade": self.cidade,
            "cep": self.cep,
            "endereco_formatado": self.endereco_formatado(),
        }


class Aluno:
    """Representa um aluno. Possui um Endereço por Agregação."""

    def __init__(self, nome: str, matricula: str, endereco: Endereco):
        self.id = None
        self.nome = nome
        self.matricula = matricula
        self.endereco = endereco

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "matricula": self.matricula,
            "endereco": self.endereco.to_dict() if self.endereco else None,
        }
