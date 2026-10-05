class SalaDeAula:
    """Representa uma sala de aula. Faz parte da Escola (Composição)."""

    def __init__(self, numero: str, capacidade: int):
        self.id: int | None = None
        self.numero: str = numero
        self.capacidade: int = capacidade

    def tem_vagas(self, qtd_alunos: int = 0) -> bool:
        if qtd_alunos < 0:
            return False
        return qtd_alunos < self.capacidade

    def to_dict(self) -> dict:
        return {"id": self.id, "numero": self.numero, "capacidade": self.capacidade}
