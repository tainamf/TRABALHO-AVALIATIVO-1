from pydantic import BaseModel, Field
from typing import Optional


class EscolaCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    cnpj: str = Field(min_length=14, max_length=18)


class SalaCreate(BaseModel):
    numero: str
    capacidade: int = Field(gt=0)


class ProfessorCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=80)
    disciplina: str = Field(min_length=2, max_length=50)


class VinculoProfessor(BaseModel):
    professor_id: int = Field(gt=0)


class EnderecoCreate(BaseModel):
    rua: str = Field(min_length=2)
    numero: str = Field(min_length=1)
    cidade: str = Field(min_length=2)
    cep: str = Field(min_length=8, max_length=9)


class AlunoCreate(BaseModel):
    nome: str = Field(min_length=3)
    matricula: str = Field(min_length=5)
    endereco_id: Optional[int] = None
    endereco: Optional[EnderecoCreate] = None
