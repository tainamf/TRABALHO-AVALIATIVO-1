from typing import List, Optional


class SalaDeAula:
    """Representa uma sala de aula. Faz parte da Escola (Composição)."""

    def __init__(self, numero: str, capacidade: int):
        self.id: Optional[int] = None
        self.numero: str = numero
        self.capacidade: int = capacidade

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "numero": self.numero,
            "capacidade": self.capacidade
        }


class Professor:
    """Representa um professor. Existe independentemente da Escola (Associação)."""

    def __init__(self, nome: str, disciplina: str):
        self.id: Optional[int] = None
        self.nome: str = nome
        self.disciplina: str = disciplina
        self.escolas_ids: List[int] = []

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "disciplina": self.disciplina,
            "escolas_ids": self.escolas_ids.copy()
        }


class Escola:
    """Representa uma escola. Cria suas salas internamente (Composição)."""

    def __init__(self, nome: str, cnpj: str):
        self.id: Optional[int] = None
        self.nome: str = nome
        self.cnpj: str = cnpj
        self.salas: List[SalaDeAula] = []
        self.professores_ids: List[int] = []

    def adicionar_sala(self, numero: str, capacidade: int) -> SalaDeAula:
        """Cria uma sala de aula dentro da escola (Composição)."""
        sala = SalaDeAula(numero, capacidade)
        self.salas.append(sala)
        return sala

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "salas": [s.to_dict() for s in self.salas],
            "professores_ids": self.professores_ids.copy()
        }


class Endereco:
    """Representa um endereço. Pode existir independentemente do Aluno (Agregação)."""

    def __init__(self, rua: str, numero: str, cidade: str, cep: str):
        self.id: Optional[int] = None
        self.rua: str = rua
        self.numero: str = numero
        self.cidade: str = cidade
        self.cep: str = cep

    def endereco_formatado(self) -> str:
        return f"{self.rua}, {self.numero} - {self.cidade}, CEP: {self.cep}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "rua": self.rua,
            "numero": self.numero,
            "cidade": self.cidade,
            "cep": self.cep,
            "endereco_formatado": self.endereco_formatado()
        }


class Aluno:
    """Representa um aluno. Possui um Endereço por Agregação."""

    def __init__(self, nome: str, matricula: str, endereco: Endereco):
        self.id: Optional[int] = None
        self.nome: str = nome
        self.matricula: str = matricula
        self.endereco: Endereco = endereco

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "matricula": self.matricula,
            "endereco": self.endereco.to_dict() if self.endereco else None
        }
