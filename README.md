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

## Executável Windows

O executável para usuários finais será disponibilizado na página de [Releases do projeto](https://github.com/kaykymnz/controle-estoque/releases). Ainda não há uma versão publicada para download.

Para publicar a primeira versão:

1. Gere e valide o executável Windows. Os arquivos e artefatos locais de build ficam em `dir_exe/`, que é ignorada pelo Git e não faz parte do repositório.
2. No GitHub, abra **Releases** e escolha **Draft a new release**.
3. Crie/escolha a tag `v0.1.0`, correspondente à versão atual do projeto, e selecione a branch/commit da primeira versão.
4. Informe o título da release, por exemplo `Controle de Estoque v0.1.0`.
5. Anexe `ControleEstoque.exe` como arquivo da release. Não adicione o binário ao commit nem ao histórico Git.
6. Revise as notas e publique a release. O link de Releases acima passa a mostrar a versão para download.

O executável deve ser gerado em Windows e inclui o Python para que a máquina de destino não precise instalá-lo. Os dados ficam fora do programa em `%LOCALAPPDATA%\ControleEstoque\data`.

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
