# Trabalho Prático 01 - Arquitetura de Software

## Objetivo

Demonstrar os conceitos de **Associação**, **Agregação** e **Composição** aplicados ao cenário de uma escola.

## Entidades

- Escola
- Sala de Aula
- Professor
- Aluno
- Endereço

## Relacionamentos

1. **Escola – Sala de Aula (Composição)**  
   A sala não faz sentido sem a escola. Por isso, a `Escola` cria a `SalaDeAula` internamente no método `adicionar_sala()`.

2. **Escola – Professor (Associação)**  
   São entidades independentes. O vínculo acontece entre objetos já existentes, podendo ser feito em ambos os sentidos.

3. **Aluno – Endereço (Agregação)**  
   O endereço pode existir independentemente do aluno. Ele é criado fora da classe `Aluno` e passado para ela.

## Execução

```bash
python3 main.py
```

## Arquivos

- `main.py` – Classes, justificativas e demonstração prática.
- `README.md` – Explicação do trabalho.
