# Trabalho Prático 01 – Arquitetura de Software

Sistema para gerenciamento de uma escola, desenvolvido com **FastAPI** para demonstrar os conceitos de **Associação**, **Agregação** e **Composição** entre entidades.

## Cenário

1. **Escola – Sala de Aula (Composição):** Uma escola possui várias salas de aula, que não fazem sentido de existir sem a escola. Caso a escola seja fechada, as salas deixam de existir no sistema.
2. **Escola – Professor (Associação):** Um professor pode lecionar em várias escolas diferentes, e uma escola pode ter vários professores. A existência de um não depende da existência do outro.
3. **Aluno – Endereço (Agregação):** O endereço é criado junto com o cadastro do aluno e só existe porque o aluno existe, mas, se o aluno for removido, o endereço pode continuar a fazer sentido isoladamente (reutilizável em relatórios/outros contextos).

## Estrutura do Projeto

```text
trab_arquitetura_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       ├── api_router.py
│   │       └── endpoints/
│   │           ├── alunos.py
│   │           ├── enderecos.py
│   │           ├── escolas.py
│   │           └── professores.py
│   ├── core/
│   │   └── exceptions.py
│   ├── models/
│   │   ├── aluno.py
│   │   ├── endereco.py
│   │   ├── escola.py
│   │   ├── professor.py
│   │   └── sala_de_aula.py
│   ├── schemas/
│   │   ├── aluno.py
│   │   ├── endereco.py
│   │   ├── escola.py
│   │   ├── professor.py
│   │   └── sala_de_aula.py
│   ├── services/
│   │   ├── aluno_service.py
│   │   ├── endereco_service.py
│   │   ├── escola_service.py
│   │   └── professor_service.py
│   └── repositories/
│       └── memoria.py
├── requirements.txt
└── README.md
```

## Como Executar

1. **Criar ambiente virtual (recomendado)**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. **Instalar dependências**

```bash
pip install -r requirements.txt
```

3. **Executar a aplicação**

```bash
uvicorn app.main:app --reload
```

4. **Acessar a documentação**

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Demonstração dos Relacionamentos

### 1. Composição – Escola ↔ Sala de Aula
- **Princípio:** A sala **não existe** sem a escola. Seu ciclo de vida depende do todo.
- **Implementação:** `Escola.adicionar_sala()` **instancia** `SalaDeAula` internamente. A criação ocorre **dentro** da escola.
- **Endpoint:** `POST /api/v1/escolas/{escola_id}/salas`

### 2. Associação – Escola ↔ Professor
- **Princípio:** Independência total. Podem existir separadamente e serem vinculados/desvinculados livremente (N:M).
- **Implementação:** Professores são criados **fora** da escola e vinculados via IDs. Ambos mantêm seus ciclos de vida independentes.
- **Endpoints:** `POST /api/v1/professores`, `POST /api/v1/escolas/{escola_id}/professores`, `DELETE /api/v1/escolas/{escola_id}/professores/{professor_id}`

### 3. Agregação – Aluno ↔ Endereço
- **Princípio:** O endereço existe junto ao aluno, mas **sobrevive** à remoção do aluno (pode ser reutilizado).
- **Implementação:** O `Endereco` é criado **fora** da classe `Aluno` e passado (ou reutilizado via `endereco_id`). Ao remover o aluno, o endereço **não é excluído**.
- **Endpoints:** `POST /api/v1/enderecos`, `POST /api/v1/alunos`, `DELETE /api/v1/alunos/{aluno_id}`
