from fastapi import FastAPI, HTTPException, status

from app.models import Escola, SalaDeAula, Professor, Endereco, Aluno
from app.schemas import (
    EscolaCreate,
    SalaCreate,
    ProfessorCreate,
    EnderecoCreate,
    AlunoCreate,
    VinculoProfessor,
)

app = FastAPI(
    title="Trabalho Prático 01 - Arquitetura de Software",
    description="Demonstração de Associação, Agregação e Composição",
    version="1.0.0",
)

# Banco em memória
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
        "mensagem": "API para demonstrar Associação, Agregação e Composição",
        "docs": "/docs",
        "composicao": "POST /escolas/{id}/salas",
        "associacao": "POST /escolas/{id}/professores",
        "agregacao": "POST /alunos",
    }


# ESCOLAS
@app.post("/escolas", status_code=status.HTTP_201_CREATED)
def criar_escola(data: EscolaCreate):
    global id_escola
    escola = Escola(data.nome, data.cnpj)
    escola.id = id_escola
    id_escola += 1
    escolas.append(escola)
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


# COMPOSIÇÃO: Sala criada DENTRO da escola
@app.post("/escolas/{escola_id}/salas", status_code=status.HTTP_201_CREATED)
def criar_sala(escola_id: int, data: SalaCreate):
    global id_sala
    for e in escolas:
        if e.id == escola_id:
            sala = e.adicionar_sala(data.numero, data.capacidade)
            sala.id = id_sala
            id_sala += 1
            return {
                "mensagem": "Sala criada por COMPOSIÇÃO (depende da escola)",
                "escola": e.to_dict(),
                "sala": sala.to_dict(),
            }
    raise HTTPException(status_code=404, detail="Escola não encontrada")


@app.get("/escolas/{escola_id}/salas")
def listar_salas(escola_id: int):
    for e in escolas:
        if e.id == escola_id:
            return {"escola": e.nome, "salas": [s.to_dict() for s in e.salas]}
    raise HTTPException(status_code=404, detail="Escola não encontrada")


# PROFESSORES
@app.post("/professores", status_code=status.HTTP_201_CREATED)
def criar_professor(data: ProfessorCreate):
    global id_professor
    prof = Professor(data.nome, data.disciplina)
    prof.id = id_professor
    id_professor += 1
    professores.append(prof)
    return prof.to_dict()


@app.get("/professores")
def listar_professores():
    return [p.to_dict() for p in professores]


# ASSOCIAÇÃO: Vincular professor à escola
@app.post("/escolas/{escola_id}/professores", status_code=status.HTTP_200_OK)
def vincular(escola_id: int, data: VinculoProfessor):
    escola = next((e for e in escolas if e.id == escola_id), None)
    prof = next((p for p in professores if p.id == data.professor_id), None)

    if not escola:
        raise HTTPException(status_code=404, detail="Escola não encontrada")
    if not prof:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    if prof.id in escola.professores_ids:
        raise HTTPException(status_code=400, detail="Professor já vinculado à escola")

    escola.professores_ids.append(prof.id)
    prof.escolas_ids.append(escola.id)

    return {
        "mensagem": "Vínculo por ASSOCIAÇÃO (independentes entre si)",
        "escola": {"id": escola.id, "nome": escola.nome},
        "professor": {"id": prof.id, "nome": prof.nome},
    }


@app.delete("/escolas/{escola_id}/professores/{professor_id}", status_code=status.HTTP_200_OK)
def desvincular(escola_id: int, professor_id: int):
    escola = next((e for e in escolas if e.id == escola_id), None)
    prof = next((p for p in professores if p.id == professor_id), None)

    if not escola or not prof:
        raise HTTPException(status_code=404, detail="Escola ou professor não encontrado")

    if prof.id not in escola.professores_ids:
        raise HTTPException(status_code=400, detail="Não há vínculo entre eles")

    escola.professores_ids.remove(prof.id)
    prof.escolas_ids.remove(escola.id)

    return {
        "mensagem": "Desvinculado. Escola e professor continuam existindo (ASSOCIAÇÃO)",
        "escola_id": escola.id,
        "professor_id": prof.id,
    }


# ENDEREÇOS
@app.post("/enderecos", status_code=status.HTTP_201_CREATED)
def criar_endereco(data: EnderecoCreate):
    global id_endereco
    end = Endereco(data.rua, data.numero, data.cidade, data.cep)
    end.id = id_endereco
    id_endereco += 1
    enderecos.append(end)
    return end.to_dict()


@app.get("/enderecos")
def listar_enderecos():
    return [e.to_dict() for e in enderecos]


# ALUNOS - AGREGAÇÃO
@app.post("/alunos", status_code=status.HTTP_201_CREATED)
def criar_aluno(data: AlunoCreate):
    global id_aluno, id_endereco

    if data.endereco_id and data.endereco:
        raise HTTPException(status_code=400, detail="Use apenas endereco_id OU endereco")

    if data.endereco_id:
        end = next((e for e in enderecos if e.id == data.endereco_id), None)
        if not end:
            raise HTTPException(status_code=404, detail="Endereço não encontrado")
        endereco_obj = end
    elif data.endereco:
        endereco_obj = Endereco(
            data.endereco.rua,
            data.endereco.numero,
            data.endereco.cidade,
            data.endereco.cep,
        )
        endereco_obj.id = id_endereco
        id_endereco += 1
        enderecos.append(endereco_obj)
    else:
        raise HTTPException(status_code=400, detail="Informe endereco_id ou endereco")

    aluno = Aluno(data.nome, data.matricula, endereco_obj)
    aluno.id = id_aluno
    id_aluno += 1
    alunos.append(aluno)

    return {
        "mensagem": "Aluno criado por AGREGAÇÃO. Endereço pode existir sem aluno.",
        "aluno": aluno.to_dict(),
    }


@app.get("/alunos")
def listar_alunos():
    return [a.to_dict() for a in alunos]


@app.delete("/alunos/{aluno_id}", status_code=status.HTTP_200_OK)
def remover_aluno(aluno_id: int):
    for i, a in enumerate(alunos):
        if a.id == aluno_id:
            endereco_salvo = a.endereco
            del alunos[i]
            return {
                "mensagem": "Aluno removido",
                "observacao": "AGREGAÇÃO: endereço NÃO foi removido (continua existindo)",
                "endereco_ainda_existente": endereco_salvo.to_dict(),
                "enderecos_restantes": len(enderecos),
            }
    raise HTTPException(status_code=404, detail="Aluno não encontrado")
