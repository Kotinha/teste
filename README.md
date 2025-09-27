# Sistema de Gestão de Igrejas

Este projeto oferece uma API completa para controle de igrejas, membros, ministérios, contribuições financeiras e eventos. A aplicação foi construída com [FastAPI](https://fastapi.tiangolo.com/) e utiliza SQLite como banco de dados padrão.

## Funcionalidades

- Cadastro de igrejas com informações de contato.
- Registro e gerenciamento de ministérios vinculados a cada igreja.
- Cadastro completo de membros, incluindo vínculos com ministérios e controle de situação ativa.
- Lançamento e consulta de dízimos por membro.
- Lançamento e consulta de ofertas por igreja ou ministério.
- Cadastro de eventos com controle de presença dos membros.
- Dashboard consolidado com indicadores de membros, contribuições e eventos futuros.

## Executando o projeto

1. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o servidor**

   ```bash
   uvicorn app.main:app --reload
   ```

3. **Acesse a documentação interativa**

   Abra o navegador em [http://localhost:8000/docs](http://localhost:8000/docs) para interagir com a API utilizando a interface Swagger.

## Estrutura principal

```
app/
  ├── crud.py           # Regras de negócio e operações no banco de dados
  ├── database.py       # Configuração do SQLAlchemy e sessão
  ├── dependencies.py   # Dependências reutilizáveis do FastAPI
  ├── main.py           # Criação da aplicação FastAPI e registro das rotas
  ├── models.py         # Modelos ORM do SQLAlchemy
  ├── routers/          # Agrupamento das rotas por domínio
  └── schemas.py        # Modelos Pydantic para validação e resposta da API
```

## Próximos passos sugeridos

- Implementar autenticação e autorização para perfis de acesso distintos (administração, liderança, membros).
- Adicionar testes automatizados para garantir a qualidade das rotas e das regras de negócio.
- Criar relatórios financeiros avançados com filtros por período e categorias personalizadas.
- Internacionalizar mensagens de erro e resposta conforme a necessidade de cada comunidade.
