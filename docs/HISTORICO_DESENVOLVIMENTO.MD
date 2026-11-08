# Histórico de Desenvolvimento

Este documento registra as solicitações do usuário, atividades realizadas pela IA, dúvidas levantadas e decisões/respostas do usuário. O histórico deve ser atualizado durante o desenvolvimento, sem apagar decisões anteriores.

## Etapa 01 — Metodologia e escopo inicial

### Interação 01 — Metodologia de trabalho

**Solicitação do usuário:**
A IA será responsável por gerar o código. O usuário conduzirá o projeto por meio de decisões, requisitos e validações. Todas as interações relevantes deverão ser documentadas.

**Atividade realizada pela IA:**  
Proposta de fluxo com levantamento de requisitos, refinamento, questionamentos técnicos, implementação, validação e documentação.

**Decisão do usuário:**  
Manter arquivos Markdown independentes para requisitos, decisões técnicas e histórico de desenvolvimento. Esta conversa será dedicada exclusivamente à documentação e planejamento; a implementação será conduzida pelo Codex em outro momento.

### Interação 02 — Definição tecnológica e requisitos iniciais

**Solicitação do usuário:**  
Desenvolver sistema de controle de estoque em Python, com interface visual, persistência JSON, executável Windows e documentação para execução pelo VS Code.

**Atividade realizada pela IA:**  
Refinamento das oito solicitações iniciais em requisitos funcionais e não funcionais.

**Decisões do usuário:**
- Python como linguagem.
- Aplicação gráfica, não dependente de CMD para operação.
- JSON como persistência inicial.
- Arquitetura preparada para futura integração com banco.
- Distribuição de executável para Windows sem exigir Python na máquina de destino.
- Documentação de execução pelo VS Code.
- Produtos: cadastrar, editar, consultar e excluir logicamente.
- Movimentações: criar, consultar, editar e excluir.
- Entrada/saída acessível também pela consulta do produto.
- Dashboard com últimas movimentações e produtos com estoque inferior a cinco unidades.

## Etapa 02 — Modelagem inicial de produtos e persistência

### Interação 03 — SKU e campos de produto

**Solicitação do usuário:**  
Utilizar SKU em vez de ID. Manter um JSON separado com identificadores para evitar percorrer um arquivo grande de produtos na validação de duplicidade. Não incluir estoque mínimo. Priorizar JSONs bem separados e organizados em pastas.

**Atividade realizada pela IA:**  
Proposta de registros individuais, índice de SKUs particionado por hash, exclusão lógica e separação entre identificador de negócio e caminho físico do arquivo.

**Decisões do usuário:**
- SKU será o identificador do produto.
- Não haverá estoque mínimo.
- O saldo não será informado livremente no cadastro; será controlado por movimentações.
- O armazenamento deverá ser dividido em arquivos e pastas organizados.

### Interação 04 — Modalidade e formato do SKU

**Dúvida retornada ao usuário:**  
O SKU será manual, automático ou ambas as opções? Qual formato será permitido?

**Resposta do usuário:**  
Ambas as opções; formato alfanumérico.

**Atividade realizada pela IA:**  
Definição de normalização para maiúsculas, reserva permanente de SKU após exclusão lógica e geração automática no formato `PRD-XXXXXXXX`, com verificação de unicidade.

## Etapa 03 — Fechamento do baseline técnico

### Interação 05 — Interface, regras e preparação para Codex

**Solicitação do usuário:**  
Seguir as recomendações técnicas pendentes, escolher a opção visual mais leve e preparar uma pasta `instructions` com documentos suficientes para o Codex compreender o projeto e iniciar a implementação.

**Atividade realizada pela IA:**  
Definição de Tkinter + ttk como interface leve, PyInstaller para empacotamento Windows e refinamento das regras de movimentação, persistência, testes, organização de dados e critérios de aceite.

**Decisões técnicas consolidadas:**
- Tkinter + ttk.
- PyInstaller, inicialmente em modo `--onefile --windowed`.
- Registros individuais de produtos e movimentações.
- Índices particionados e reconstruíveis.
- Movimentações ativas como fonte oficial do saldo.
- Saldo negativo proibido.
- Quantidades inteiras positivas.
- Exclusão lógica de produtos e movimentações.
- Produto só pode ser excluído com saldo zero.
- Movimentação editada não pode trocar o SKU relacionado.
- Dados da versão empacotada em diretório do usuário, fora do executável.
- Uso local por uma única instância no MVP.

**Resultado:**  
Baseline documental e pacote de instruções para o Codex preparados. As definições deste baseline devem ser respeitadas; dúvidas ou conflitos devem ser apresentados ao usuário antes de alterar regras.

## Etapa 04 — Início da implementação

### Interação 06 — Decisões para a Fase 1

**Solicitação do usuário:**
Informou que os documentos faltantes foram incluídos, escolheu `pytest` como ferramenta de testes e determinou que arquivos JSON inválidos devem informar o arquivo afetado. Autorizou o prosseguimento sem lacunas pendentes.

**Atividade realizada pela IA/Codex:**
Releitura do baseline consolidado e início da Fase 1, com estrutura mínima de pacotes, modelos de domínio, contratos de repositório, resolução de diretórios e janela Tkinter inicial.

**Decisão do usuário:**
- Usar `pytest`.
- Informar o caminho do JSON inválido, sem recuperação automática.
- Prosseguir com a implementação.

**Validação:**
`py -m pytest -q`: 9 testes aprovados. A criação e destruição programática da janela Tkinter também foi verificada sem erro.

**Documentos atualizados:**
`docs/DECISOES_TECNICAS.md`, este histórico, `pyproject.toml`, `src/` e `tests/`.

### Interação 07 — Fase 2: persistência JSON

**Solicitação do usuário:**
Após validar visualmente a fundação, solicitou o avanço para a próxima etapa e reforçou o cumprimento dos acordos documentados.

**Atividade realizada pela IA/Codex:**
Implementação da persistência JSON isolada da interface: leitura com erro acionável, escrita temporária seguida de `os.replace`, serializadores para `Product` e `Movement`, registros individuais, registro de SKU e índice de movimentações por produto. Também foi incluída a reconstrução de índices, com descarte dos shards derivados obsoletos, e a reconciliação do cache de saldo a partir do ledger ativo.

**Decisão técnica aplicada:**
Os caches `__pycache__` e `.pytest_cache` são gerados automaticamente pelo Python/pytest, são descartáveis e passaram a ser ignorados pelo Git.

**Validação:**
`py -m pytest -q`: 15 testes aprovados. A suíte cobre persistência após recriar repositórios, escrita sem arquivo temporário remanescente, reconstrução de índices, remoção de shards obsoletos, reconciliação de saldo e mensagem com o caminho de JSON inválido.

**Documentos atualizados:**
Este histórico e `.gitignore`.

### Interação 08 — Fase 3: regras de negócio

**Solicitação do usuário:**
Após confirmar que a janela inicial abriu corretamente, solicitou o avanço para a próxima fase, mantendo as decisões de produto sob sua responsabilidade.

**Atividade realizada pela IA/Codex:**
Implementação dos serviços de produtos e movimentações. Foram incluídos cadastro por SKU manual ou automático, normalização, reserva permanente de SKU, edição de campos permitidos, exclusão lógica condicionada a saldo zero, entrada, saída, edição, cancelamento e atualização consistente do cache de saldo. A consulta de produto passou a localizar o registro canônico mesmo se o índice de SKU estiver ausente.

**Decisão técnica aplicada:**
Nenhuma decisão de escopo ou regra de produto foi adicionada. A tela permanece como marco temporário da fundação até a Fase 4 conectar os serviços à interface gráfica.

**Validação:**
`py -m pytest -q`: 23 testes aprovados. A suíte valida SKU manual e automático, colisão de SKU automático, duplicidade após exclusão lógica, edição permitida, entradas, saídas, bloqueio de saldo negativo, edição/cancelamento de movimentação, cancelamento de entrada que deixaria saldo negativo e bloqueio de nova movimentação para produto excluído.

**Documentos atualizados:**
Este histórico.

### Interação 09 — Alteração de SKU e confirmação arquitetural

**Solicitação do usuário:**
Alterar a regra para SKU exclusivamente automático, atualizar todo o projeto e a documentação, e confirmar a arquitetura adotada.

**Decisão do usuário:**
- SKU sempre automático.
- Manter a arquitetura em camadas atual; não migrar para MVC.

**Atividade realizada pela IA/Codex:**
Remoção da entrada manual de SKU no serviço, interface, testes e documentos. Confirmação da arquitetura de apresentação, aplicação, domínio e infraestrutura JSON.

**Validação:**
`py -m pytest -q`: 22 testes aprovados após a alteração.

**Documentos atualizados:**
`docs/REQUISITOS.md`, `docs/DECISOES_TECNICAS.md`, `instructions/` e este histórico.

### Interação 10 — Fase 5: validação integrada

**Solicitação do usuário:**
Avançar para a etapa de integração e validação.

**Atividade realizada pela IA/Codex:**
Execução da suíte automatizada, compilação dos módulos e fluxo integrado isolado em diretório temporário: cadastro automático de produto, entrada, saída, edição, cancelamento, nova saída, exclusão lógica e leitura por repositórios recriados.

**Validação:**
- `py -m pytest -q`: 22 testes aprovados.
- `py -m compileall -q src`: concluído sem erros.
- Fluxo integrado: aprovado, com saldo reconciliado e persistência validada após recriar os repositórios.

**Documentos atualizados:**
Este histórico.

### Interação 11 — Refinamento de cadastro, filtros e validações

**Solicitação do usuário:**
Documentar e implementar os pontos pendentes: impedir saída acima do estoque disponível, permitir categoria no cadastro, oferecer filtros por coluna e confirmar que exclusão é somente lógica.

**Análise da IA/Codex:**
O bloqueio de saldo negativo e a exclusão lógica já estavam implementados e testados na camada de aplicação. As lacunas identificadas são de interface: o diálogo de cadastro ainda não solicitava categoria e a listagem ainda não expunha filtros visuais.

**Escopo aprovado para a etapa:**
- Manter saída bloqueada quando exceder o saldo, exibindo mensagem gráfica em português.
- Incluir categoria opcional no cadastro de produto.
- Adicionar filtros visuais às consultas de produtos e movimentações.
- Manter exclusão física fora do fluxo da aplicação; a ação de excluir continuará sendo soft delete.

**Validação:**
Pendente após a implementação.

**Documentos atualizados:**
Este histórico; os requisitos e decisões existentes já contemplam essas regras e serão mantidos consistentes durante a implementação.

### Interação 12 — Categoria na edição de produto

**Solicitação do usuário:**
Incluir a categoria no fluxo de edição de produtos.

**Atividade realizada pela IA/Codex:**
Adição de campo gráfico opcional de categoria no diálogo de edição. SKU e saldo continuam preservados e não editáveis.

**Validação:**
Pendente da execução da suíte após a alteração.

**Documentos atualizados:**
Este histórico.

### Interação 13 — Ajuste do dashboard

**Solicitação do usuário:**
Finalizar o dashboard com o quadro “Últimas movimentações”, limitado às 5 mais recentes, e o quadro “Produtos com saldo baixo”, contendo produtos com saldo menor que 5.

**Decisão do usuário:**
Alterar o limite anterior de 10 para 5 movimentações recentes.

**Atividade realizada pela IA/Codex:**
Atualização da documentação de requisitos, instruções e decisão técnica antes do ajuste visual.

**Validação:**
Pendente após a implementação da interface.

**Documentos atualizados:**
`docs/REQUISITOS.md`, `docs/DECISOES_TECNICAS.md`, `instructions/01_CONTEXTO_E_ESCOPO.md`, `instructions/02_REGRAS_DE_NEGOCIO.md` e este histórico.

### Interação 14 — Fase 6: distribuição Windows e documentação final

**Solicitação do usuário:**
Retomar a etapa de distribuição com PyInstaller após leitura das instruções e documentos, preservar a estrutura existente, manter todos os arquivos necessários ao executável em `dir_exe/` e registrar os problemas encontrados como ajustes para a V2.

**Atividade realizada pela IA/Codex:**
- Adicionados em `dir_exe/` o spec do PyInstaller, a lista de dependências de build e um script PowerShell que cria ambiente isolado, instala o PyInstaller e gera `ControleEstoque.exe` em modo `--onefile --windowed`.
- Ajustada a resolução de dados empacotados para respeitar `LOCALAPPDATA`, mantendo `data/` na raiz durante o desenvolvimento.
- Atualizado o README com execução pelo VS Code, testes, dados, geração local do executável e link da página de Releases.
- Documentados os itens de melhoria identificados na revisão anterior como backlog da V2, sem incorporá-los ao comportamento desta versão.

**Dúvidas e decisões:**
Nenhuma pergunta foi necessária. A geração local foi mantida separada da publicação de uma release, que requer validação e publicação próprias.

**Validação:**
- `python -m pytest -q`: 25 testes aprovados.
- Build PyInstaller executado em Windows com Python 3.14.3; gerado `dir_exe/dist/ControleEstoque.exe` (~12,8 MB), modo `--onefile --windowed`.
- Teste de fumaça: executável abriu e permaneceu ativo por cinco segundos usando diretório `LOCALAPPDATA` temporário; processo encerrado e dados temporários removidos.
- O teste em Windows sem Python instalado ainda não foi realizado; validar em máquina limpa antes de publicar uma release.

**Documentos/arquivos atualizados:**
`README.md`, `docs/REQUISITOS.MD`, `docs/ARQUITETURA_E_DADOS.md`, `docs/DECISOES_TECNICAS.MD`, este histórico, `instructions/06_DOCUMENTACAO_E_ENTREGA.md`, `.gitignore`, `src/controle_estoque/app/paths.py`, `tests/test_paths.py` e os arquivos de build em `dir_exe/`.

### Interação 15 — Preparação do repositório e publicação do executável

**Solicitação do usuário:**
Ignorar `dir_exe/` no Git e receber orientação para disponibilizar o executável na página do projeto no GitHub.

**Resposta/decisão do usuário:**
O usuário final poderá clonar o repositório para executar o projeto pelo VS Code, mas quem quiser usar o programa como `.exe` deverá baixá-lo; os scripts locais de build não precisam ser distribuídos no repositório.

**Atividade realizada pela IA/Codex:**
- Adicionada a regra `dir_exe/` ao `.gitignore`.
- Ajustada a documentação para distinguir o código-fonte, os arquivos locais de build e o executável publicado como anexo de Release.
- Incluído no README o procedimento de criação da primeira release com a tag `v0.1.0`, correspondente à versão atual do `pyproject.toml`.
- A página Releases ainda não foi criada/publicada; o executável precisa ser anexado pelo mantenedor após a validação final em Windows sem Python.

**Validação:**
- `git check-ignore -v` confirmou que scripts, configuração, artefatos de build e executável em `dir_exe/` são ignorados pela regra do diretório.
- README e documentação de arquitetura distinguem a execução a partir do clone da distribuição do executável via GitHub Release.

**Documentos/arquivos atualizados:**
`.gitignore`, `README.md`, `docs/ARQUITETURA_E_DADOS.md`, `docs/DECISOES_TECNICAS.MD`, `instructions/06_DOCUMENTACAO_E_ENTREGA.md` e este histórico.

## Modelo para próximas interações

### Interação NN — [Título]

**Solicitação do usuário:**  
[Registrar a solicitação original.]

**Atividade realizada pela IA/Codex:**  
[Descrever o que foi realizado.]

**Dúvida retornada ao usuário:**  
[Registrar pergunta técnica/funcional, se houver.]

**Resposta do usuário:**  
[Registrar a decisão.]

**Validação:**  
[Registrar testes, evidências e resultado.]

**Documentos atualizados:**  
[Relacionar arquivos alterados.]
