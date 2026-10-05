from typing import List

from .sala_de_aula import SalaDeAula


class Escola:
    """Representa uma escola. É responsável por criar suas salas (Composição)."""

    def __init__(self, nome: str, cnpj: str):
        self.id: int | None = None
        self.nome: str = nome
        self.cnpj: str = cnpj
        self.salas: List[SalaDeAula] = []
        self.professores_ids: List[int] = []

    def adicionar_sala(self, numero: str, capacidade: int) -> SalaDeAula:
        sala = SalaDeAula(numero, capacidade)
        self.salas.append(sala)
        return sala

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "salas": [s.to_dict() for s in self.salas],
            "professores_ids": self.professores_ids.copy(),
        }
