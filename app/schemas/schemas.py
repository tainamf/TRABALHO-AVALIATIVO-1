from pydantic import BaseModel, Field
from typing import Optional


class EscolaCreate(BaseModel):
    nome: str = Field(min_length=3)
    cnpj: str = Field(min_length=14, max_length=18)


class SalaCreate(BaseModel):
    numero: str
    capacidade: int = Field(gt=0)


class ProfessorCreate(BaseModel):
    nome: str
    disciplina: str


class EnderecoCreate(BaseModel):
    rua: str
    numero: str
    cidade: str
    cep: str


class AlunoCreate(BaseModel):
    nome: str
    matricula: str
    endereco_id: Optional[int] = None
    endereco: Optional[EnderecoCreate] = None


class VinculoProfessor(BaseModel):
    professor_id: int
