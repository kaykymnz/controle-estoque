# Controle de Estoque

Aplicação desktop local para cadastro de produtos e registro de entradas e saídas de estoque. Desenvolvida em Python com interface Tkinter/ttk e persistência em arquivos JSON.

## Funcionalidades

- Cadastro de produtos com SKU automático.
- Edição de dados do produto e consulta com filtros.
- Entradas, saídas, edição e cancelamento lógico de movimentações.
- Bloqueio de operações que deixariam o saldo negativo.
- Dashboard com as cinco movimentações ativas mais recentes e produtos ativos com saldo abaixo de cinco.
- Persistência local em JSON, com índices reconstruíveis.

## Tecnologias

- Python 3.11 ou superior
- Tkinter + ttk
- JSON
- pytest
- PyInstaller para distribuição Windows

## Executável Windows — V1

A versão 1.0 já está disponível para Windows.

1. Acesse a página de [Releases](https://github.com/kaykymnz/controle-estoque/releases).
2. Baixe o arquivo `ControleEstoque.exe` da versão V1.
3. Salve o arquivo em uma pasta de sua preferência e execute-o.

Não é necessário instalar Python ou as dependências do projeto para utilizar o executável.

Os dados são armazenados separadamente do programa, em `%LOCALAPPDATA%\ControleEstoque\data`. Assim, é possível atualizar o executável sem perder os dados cadastrados.

## Executar pelo VS Code

### Windows (PowerShell)

1. Instale [Python 3.11 ou superior](https://www.python.org/downloads/) e o [VS Code](https://code.visualstudio.com/). Confirme que o launcher `py` está disponível.
2. Clone o repositório e abra a pasta no VS Code:

   ```powershell
   git clone https://github.com/kaykymnz/controle-estoque.git
   cd controle-estoque
   code .
   ```

3. No terminal PowerShell do VS Code, crie e ative o ambiente virtual:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Instale o projeto e as dependências de desenvolvimento:

   ```powershell
   python -m pip install -e ".[dev]"
   ```

5. Inicie a aplicação:

   ```powershell
   python -m controle_estoque.main
   ```

### macOS/Linux

O desenvolvimento pode ser executado nessas plataformas com Python 3.11+ e Tkinter instalado:

```bash
git clone https://github.com/kaykymnz/controle-estoque.git
cd controle-estoque
code .
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m controle_estoque.main
```

O executável distribuído é destinado ao Windows.

## Testes

Com o ambiente virtual ativado e as dependências instaladas:

```powershell
python -m pytest -q
```

## Dados e arquivos

- Em desenvolvimento, os dados ficam em `data/` na raiz do repositório.
- No executável Windows, os dados ficam em `%LOCALAPPDATA%\ControleEstoque\data`.
- O executável e os dados ficam separados; atualizar o programa não deve apagar os dados do usuário.
- Toda a pasta `dir_exe/` é local e ignorada pelo Git. O `.exe` é distribuído como anexo de uma GitHub Release, não como parte do repositório.

## Limitações conhecidas e melhorias planejadas

A aplicação é local e destinada a uma instância por vez. JSON não fornece transações ACID nem coordenação de gravações simultâneas. Os pontos de melhoria identificados para a V2 estão registrados em [docs/REQUISITOS.MD](./docs/REQUISITOS.MD); eles não fazem parte desta etapa de distribuição.

O executável precisa ser validado em uma máquina Windows limpa, sem Python instalado, antes de publicar uma distribuição aprovada.

## Uso de Inteligência Artificial

Ferramentas de IA foram usadas como apoio à análise, implementação, testes e documentação. Requisitos e decisões de produto permanecem sob responsabilidade do desenvolvedor, que deve revisar e validar o código e o executável.

---

**Desenvolvido por:** Kayky Bezerra
