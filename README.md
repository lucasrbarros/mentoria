# Sistema de Gestão de Chamados para Mentoria

Sistema web para organizar e gerenciar chamados de suporte técnico, permitindo uma melhor organização do atendimento entre técnicos e seniors.

## Funcionalidades

- Cadastro de chamados com informações detalhadas
- Sistema de fila ordenada por prioridade
- Gerenciamento de status dos chamados
- Upload de prints e links
- Sistema de login e permissões

## Requisitos

- Python 3.8+
- SQLite3

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```
5. Inicialize o banco de dados:
```bash
flask db init
flask db migrate
flask db upgrade
```
6. Execute o servidor:
```bash
flask run
```

## Estrutura do Projeto

```
mentoria/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── config.py
├── requirements.txt
└── run.py
``` 