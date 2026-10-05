class Professor:
    """Representa um professor. Existe independentemente da Escola (Associação)."""

    def __init__(self, nome: str, disciplina: str):
        self.id: int | None = None
        self.nome: str = nome
        self.disciplina: str = disciplina
        self.escolas_ids: list[int] = []

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "disciplina": self.disciplina,
            "escolas_ids": self.escolas_ids.copy(),
        }
