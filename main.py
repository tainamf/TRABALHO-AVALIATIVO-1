from fastapi import FastAPI, HTTPException, status

from models import Escola, Professor, Endereco, Aluno
from app.schemas.schemas import (
    EscolaCreate,
    SalaCreate,
    ProfessorCreate,
    EnderecoCreate,
    AlunoCreate,
    VinculoProfessor,
)

app = FastAPI(
    title="Trabalho Prático 01 - Arquitetura de Software",
    description="Demonstração de Associação, Agregação e Composição com API REST",
    version="1.0.0",
)

# "Banco" em memória
escolas: list[Escola] = []
professores: list[Professor] = []
enderecos: list[Endereco] = []
alunos: list[Aluno] = []

# Contadores
id_escola = 1
id_professor = 1
id_sala = 1
id_endereco = 1
id_aluno = 1


@app.get("/")
def home():
    return {
        "mensagem": "API para demonstração dos relacionamentos: Associação, Agregação e Composição",
        "rotas": {
            "escolas": "/escolas",
            "professores": "/professores",
            "enderecos": "/enderecos",
            "alunos": "/alunos",
            "docs": "/docs",
        },
    }


# ESCOLAS
@app.post("/escolas", status_code=status.HTTP_201_CREATED)
def criar_escola(data: EscolaCreate):
    global id_escola
    escola = Escola(nome=data.nome, cnpj=data.cnpj)
    escola.id = id_escola
    escolas.append(escola)
    id_escola += 1
    return escola.to_dict()


@app.get("/escolas")
def listar_escolas():
    return [e.to_dict() for e in escolas]


@app.get("/escolas/{escola_id}")
def buscar_escola(escola_id: int):
    for e in escolas:
        if e.id == escola_id:
            return e.to_dict()
    raise HTTPException(status_code=404, detail="Escola não encontrada")


# COMPOSIÇÃO: Criar sala DENTRO da escola
@app.post("/escolas/{escola_id}/salas", status_code=status.HTTP_201_CREATED)
def criar_sala_na_escola(escola_id: int, data: SalaCreate):
    global id_sala
    for e in escolas:
        if e.id == escola_id:
            sala = e.adicionar_sala(numero=data.numero, capacidade=data.capacidade)
            sala.id = id_sala
            id_sala += 1
            return {
                "mensagem": "Sala criada por COMPOSIÇÃO (pertence unicamente à escola)",
                "escola": e.nome,
                "sala": sala.to_dict(),
            }
    raise HTTPException(status_code=404, detail="Escola não encontrada")


@app.get("/escolas/{escola_id}/salas")
def listar_salas_da_escola(escola_id: int):
    for e in escolas:
        if e.id == escola_id:
            return {"escola": e.nome, "salas": [s.to_dict() for s in e.salas]}
    raise HTTPException(status_code=404, detail="Escola não encontrada")


# PROFESSORES (Associação)
@app.post("/professores", status_code=status.HTTP_201_CREATED)
def criar_professor(data: ProfessorCreate):
    global id_professor
    prof = Professor(nome=data.nome, disciplina=data.disciplina)
    prof.id = id_professor
    professores.append(prof)
    id_professor += 1
    return prof.to_dict()


@app.get("/professores")
def listar_professores():
    return [p.to_dict() for p in professores]


# ASSOCIAÇÃO: Vincular professor à escola
@app.post("/escolas/{escola_id}/professores", status_code=status.HTTP_200_OK)
def vincular_professor(escola_id: int, data: VinculoProfessor):
    escola = next((e for e in escolas if e.id == escola_id), None)
    if not escola:
        raise HTTPException(status_code=404, detail="Escola não encontrada")

    prof = next((p for p in professores if p.id == data.professor_id), None)
    if not prof:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    if prof.id in escola.professores_ids and escola_id in prof.escolas_ids:
        raise HTTPException(status_code=400, detail="Professor já vinculado a esta escola")

    escola.professores_ids.append(prof.id)
    prof.escolas_ids.append(escola.id)

    return {
        "mensagem": "Vínculo criado por ASSOCIAÇÃO (ambos continuam independentes)",
        "escola": {"id": escola.id, "nome": escola.nome},
        "professor": {"id": prof.id, "nome": prof.nome, "disciplina": prof.disciplina},
        "vinculos": {
            "professor.escolas_ids": prof.escolas_ids,
            "escola.professores_ids": escola.professores_ids,
        },
    }


@app.post("/escolas/{escola_id}/professores/{professor_id}/desvincular", status_code=status.HTTP_200_OK)
def desvincular_professor(escola_id: int, professor_id: int):
    escola = next((e for e in escolas if e.id == escola_id), None)
    prof = next((p for p in professores if p.id == professor_id), None)

    if not escola or not prof:
        raise HTTPException(status_code=404, detail="Escola ou Professor não encontrado")

    if prof.id not in escola.professores_ids:
        raise HTTPException(status_code=400, detail="Professor não está vinculado a esta escola")

    escola.professores_ids.remove(prof.id)
    prof.escolas_ids.remove(escola.id)

    return {
        "mensagem": "Vínculo removido. Escola e Professor seguem existindo normalmente.",
        "escola_id": escola.id,
        "professor_id": prof.id,
    }


# ENDEREÇOS (Agregação)
@app.post("/enderecos", status_code=status.HTTP_201_CREATED)
def criar_endereco(data: EnderecoCreate):
    global id_endereco
    end = Endereco(rua=data.rua, numero=data.numero, cidade=data.cidade, cep=data.cep)
    end.id = id_endereco
    enderecos.append(end)
    id_endereco += 1
    return end.to_dict()


@app.get("/enderecos")
def listar_enderecos():
    return [e.to_dict() for e in enderecos]


# ALUNOS (Agregação: Endereço existe fora)
@app.post("/alunos", status_code=status.HTTP_201_CREATED)
def criar_aluno(data: AlunoCreate):
    global id_aluno, id_endereco

    endereco_obj = None

    if data.endereco_id:
        endereco_obj = next((e for e in enderecos if e.id == data.endereco_id), None)
        if not endereco_obj:
            raise HTTPException(status_code=404, detail="Endereço informado não existe")
    elif data.endereco:
        endereco_obj = Endereco(
            rua=data.endereco.rua,
            numero=data.endereco.numero,
            cidade=data.endereco.cidade,
            cep=data.endereco.cep,
        )
        endereco_obj.id = id_endereco
        enderecos.append(endereco_obj)
        id_endereco += 1
    else:
        raise HTTPException(status_code=400, detail="Informe 'endereco_id' ou 'endereco' completo")

    aluno = Aluno(nome=data.nome, matricula=data.matricula, endereco=endereco_obj)
    aluno.id = id_aluno
    alunos.append(aluno)
    id_aluno += 1

    return {
        "mensagem": "Aluno criado com AGREGAÇÃO. O endereço foi criado/reutilizado fora do Aluno.",
        "aluno": aluno.to_dict(),
    }


@app.get("/alunos")
def listar_alunos():
    return [a.to_dict() for a in alunos]


@app.delete("/alunos/{aluno_id}", status_code=status.HTTP_200_OK)
def remover_aluno(aluno_id: int):
    aluno = next((a for a in alunos if a.id == aluno_id), None)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    endereco_salvo = aluno.endereco
    alunos.remove(aluno)

    return {
        "mensagem": "Aluno removido com sucesso.",
        "observacao": "Por se tratar de AGREGAÇÃO, o endereço NÃO foi excluído e continua disponível.",
        "endereco_ainda_existente": endereco_salvo.to_dict(),
        "total_enderecos_restantes": len(enderecos),
    }
