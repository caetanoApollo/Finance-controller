# Finance Controller

O `Finance Controller` é uma aplicação em Python que auxilia na gestão financeira pessoal, permitindo o controle de transações, visualização de gráficos e categorização de despesas e receitas.

## Funcionalidades

- **Gestão de Transações:**
  - Adicionar, editar e excluir transações financeiras.
  - Filtrar transações por tipo, categoria, mês e ano.
  - Exportar dados das transações para CSV.

- **Visualização de Gráficos:**
  - Gráficos de pizza para visualização de entradas e saídas.
  - Atualização automática dos gráficos conforme os filtros aplicados.

- **Interface Gráfica:**
  - Interface intuitiva e fácil de usar desenvolvida com PyQt5.
  - Suporte a modo escuro para melhor visualização.

## Estrutura do Projeto

```
finance-controller
├── output
│   └── Gestão Financeira.exe  # Executável gerado da aplicação
├── requirements.txt           # Dependências do projeto
├── src
│   ├── charts
│   │   └── plotter.py         # Módulo para criação de gráficos
│   ├── database
│   │   └── db_manager.py      # Gerenciamento do banco de dados SQLite
│   ├── gui
│   │   └── interface.py       # Interface gráfica do usuário
│   ├── icons                  # Ícones utilizados na aplicação
│   ├── main.py                # Ponto de entrada da aplicação
│   └── utils
│       └── helpers.py         # Funções utilitárias
```

## Instalação

1. Clone o repositório:
   ```sh
   git clone <URL_DO_REPOSITORIO>
   ```

2. Navegue até o diretório do projeto:
   ```sh
   cd finance-controller
   ```

3. Crie um ambiente virtual e ative-o:
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

4. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

## Uso

Para iniciar a aplicação, execute o seguinte comando:
```sh
python src/main.py
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
