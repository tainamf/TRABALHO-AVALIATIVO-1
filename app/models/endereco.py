class Endereco:
    """Representa um endereço. Pode existir independentemente do Aluno (Agregação)."""

    def __init__(self, rua: str, numero: str, cidade: str, cep: str):
        self.id: int | None = None
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
            "endereco_formatado": self.endereco_formatado(),
        }
