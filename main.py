from typing import List


class SalaDeAula:
    def __init__(self, numero: str, capacidade: int):
        self.numero = numero
        self.capacidade = capacidade

    def tem_vagas(self, qtd_alunos: int = 0) -> bool:
        if qtd_alunos < 0:
            return False
        return qtd_alunos < self.capacidade

    def obter_informacoes(self) -> str:
        return f"Sala {self.numero} | Capacidade: {self.capacidade} alunos"

    def __str__(self):
        return self.obter_informacoes()


class Professor:
    def __init__(self, nome: str, disciplina: str):
        self.nome = nome
        self.disciplina = disciplina
        self.escolas: List['Escola'] = []

    def vincular_escola(self, escola):
        if escola not in self.escolas:
            self.escolas.append(escola)
            if self not in escola.professores:
                escola.professores.append(self)

    def desvincular_escola(self, escola):
        if escola in self.escolas:
            self.escolas.remove(escola)
            if self in escola.professores:
                escola.professores.remove(self)

    def __str__(self):
        return f"Professor(a): {self.nome} | Disciplina: {self.disciplina}"


class Escola:
    def __init__(self, nome: str, cnpj: str):
        self.nome = nome
        self.cnpj = cnpj
        self.salas: List[SalaDeAula] = []
        self.professores: List[Professor] = []

    def adicionar_sala(self, numero: str, capacidade: int):
        sala = SalaDeAula(numero, capacidade)
        self.salas.append(sala)
        return sala

    def contratar_professor(self, professor: Professor):
        if professor not in self.professores:
            self.professores.append(professor)
            if self not in professor.escolas:
                professor.escolas.append(self)

    def remover_professor(self, professor: Professor):
        if professor in self.professores:
            self.professores.remove(professor)
            if self in professor.escolas:
                professor.escolas.remove(self)

    def __str__(self):
        return f"Escola: {self.nome} | CNPJ: {self.cnpj}"


class Endereco:
    def __init__(self, rua: str, numero: str, cidade: str, cep: str):
        self.rua = rua
        self.numero = numero
        self.cidade = cidade
        self.cep = cep

    def endereco_formatado(self) -> str:
        return f"{self.rua}, {self.numero} - {self.cidade}, CEP: {self.cep}"

    def __str__(self):
        return self.endereco_formatado()


class Aluno:
    def __init__(self, nome: str, matricula: str, endereco: Endereco):
        self.nome = nome
        self.matricula = matricula
        self.endereco = endereco

    def __str__(self):
        return f"Aluno: {self.nome} | Matrícula: {self.matricula}"


if __name__ == "__main__":
    print("1. COMPOSIÇÃO (Escola - Sala de Aula)")
    escola = Escola("Escola Modelo", "12.345.678/0001-90")
    sala1 = escola.adicionar_sala("A101", 40)
    sala2 = escola.adicionar_sala("B202", 35)
    print(escola)
    print(sala1)
    print(sala2)
    print(len(escola.salas))

    print("2. ASSOCIAÇÃO (Escola - Professor)")
    prof1 = Professor("João Silva", "Matemática")
    prof2 = Professor("Maria Santos", "História")
    escola.contratar_professor(prof1)
    prof2.vincular_escola(escola)
    print(prof1)
    print(prof2)
    print(len(escola.professores))
    print(len(prof1.escolas))

    print("3. AGREGAÇÃO (Aluno - Endereço)")
    endereco = Endereco("Rua das Flores", "123", "São Paulo", "01234-567")
    aluno = Aluno("Carlos Oliveira", "20261001", endereco)
    print(aluno)
    print(endereco)
    del aluno
    print(endereco)
