# Histórico de Desenvolvimento

## Etapa 01 — Definição inicial do projeto e requisitos

### Interação 01 — Definição da metodologia

**Solicitação do usuário:**

Estabelecer uma metodologia de desenvolvimento na qual a Inteligência Artificial será responsável pela geração do código, enquanto o usuário será responsável pelas decisões, definições e validações do projeto.

Todas as interações relevantes deverão ser documentadas, incluindo solicitações, atividades realizadas, dúvidas levantadas pela IA e respostas fornecidas pelo usuário.

**Atividade realizada pela IA:**

Definição de um fluxo de trabalho baseado em levantamento de requisitos, refinamento, questionamentos técnicos, implementação, validação e documentação.

**Decisão do usuário:**

A documentação deverá ser mantida em arquivos Markdown independentes, preservando o histórico das decisões e atividades.

### Interação 02 — Definição tecnológica e escopo inicial

**Solicitação do usuário:**

Desenvolver um sistema de controle de estoque utilizando Python, com interface gráfica, armazenamento inicial em arquivos JSON e possibilidade de distribuição por meio de um executável Windows.

Também deverá existir documentação para execução do projeto pelo Visual Studio Code.

**Atividade realizada pela IA:**

Refinamento das solicitações em requisitos funcionais e não funcionais, com elaboração da primeira versão do documento `REQUISITOS.md`.

**Decisões do usuário:**

- Utilizar Python como linguagem de programação.
- Desenvolver uma aplicação visual, não limitada ao CMD.
- Utilizar arquivos JSON como persistência inicial.
- Preparar a estrutura para futura integração com banco de dados.
- Disponibilizar um executável `.exe` para usuários Windows.
- Documentar o processo de execução pelo VS Code.

**Resultado:**

Primeira versão dos requisitos funcionais e não funcionais elaborada, aguardando validação e complementação.


### Interação 03 — Definição da identificação de produtos

**Solicitação do usuário:**

Definir o SKU como identificador dos produtos, com suporte à geração automática ou preenchimento manual. O formato deverá ser alfanumérico.

Também foi solicitado um armazenamento separado contendo os identificadores, evitando percorrer todos os registros de produtos para verificar duplicidades.

**Atividade realizada pela IA:**

Refinamento da estratégia de armazenamento, propondo registros individuais, índices auxiliares, particionamento por hash e separação entre identificadores de negócio e nomes físicos dos arquivos.

**Decisões do usuário:**

- Permitir SKU manual e automático.
- Utilizar formato alfanumérico.
- Não utilizar estoque mínimo.
- Manter os registros dos produtos em arquivos separados.
- Manter um registro exclusivo de identificadores para controle de duplicidade.
- Priorizar uma estrutura de armazenamento organizada e preparada para crescimento.

**Resultado:**

Estratégia inicial de identificação e armazenamento de produtos definida.