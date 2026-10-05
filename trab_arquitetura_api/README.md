# Trabalho Prático 01 - Arquitetura de Software

API REST com FastAPI, seguindo o princípio **KISS** (Keep It Simple, Stupid).

## Entidades e Relacionamentos

- **Escola – Sala de Aula**: **Composição**. A sala é criada DENTRO da escola. Não existe sem a escola.
- **Escola – Professor**: **Associação**. Existem de forma independente e são vinculados/desvinculados.
- **Aluno – Endereço**: **Agregação**. O endereço existe fora do aluno e **sobrevive** quando o aluno é removido.

## Estrutura (KISS)

```text
trab_arquitetura_api/
├── app/
│   ├── main.py      # Rotas e lógica da API
│   └── models.py    # Classes (domínio)
│   └── schemas.py   # Schemas Pydantic
├── requirements.txt
└── README.md
```

## Execução

```bash
cd trab_arquitetura_api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
