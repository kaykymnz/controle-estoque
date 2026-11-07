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
