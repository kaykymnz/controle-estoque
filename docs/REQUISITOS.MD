# Requisitos do Sistema — Controle de Estoque

**Projeto:** Controle de Estoque  
**Linguagem:** Python  
**Tipo:** Aplicação desktop com interface gráfica  
**Persistência inicial:** Arquivos JSON  
**Status:** Baseline inicial para implementação

## 1. Objetivo

Desenvolver uma aplicação desktop para gerenciamento de produtos e movimentações de estoque. O sistema deve permitir cadastrar e consultar produtos, registrar entradas e saídas, consultar o histórico de movimentações e acompanhar informações relevantes em um dashboard.

A primeira versão será local e utilizará arquivos JSON. A estrutura deverá isolar a persistência para permitir uma futura substituição por banco de dados.

## 2. Requisitos funcionais

### RF01 — Cadastro de produtos
O sistema deve permitir cadastrar produtos com os campos:
- SKU: obrigatório e único;
- nome: obrigatório;
- descrição: opcional;
- categoria: opcional, texto livre;
- preço de custo: opcional, não negativo;
- preço de venda: opcional, não negativo;
- data de criação: gerada automaticamente;
- data de atualização: gerada/atualizada automaticamente;
- status de exclusão lógica;
- saldo atual: valor derivado das movimentações, mantido como cache para consulta.

O SKU será sempre gerado automaticamente pelo sistema no formato `PRD-XXXXXXXX`. O SKU será normalizado para maiúsculas e não poderá ser alterado pela edição convencional.

### RF02 — Edição de produtos
Permitir editar nome, descrição, categoria e preços. Não permitir alterar SKU nem editar diretamente o saldo de estoque.

### RF03 — Consulta e filtros de produtos
Permitir consultar produtos ativos e, mediante opção específica, produtos excluídos logicamente. Filtros mínimos:
- SKU;
- nome;
- categoria;
- situação do estoque: todos, zerado ou positivo;
- incluir produtos excluídos.

Colunas padrão da listagem: SKU, nome, categoria, preço de custo, preço de venda, saldo atual e situação.

### RF04 — Exclusão lógica de produtos
A exclusão deve ser lógica, sem apagar o registro físico. Produtos excluídos não aparecem nas consultas convencionais e não aceitam novas movimentações. Para preservar a consistência, a exclusão será permitida somente quando o saldo atual for zero. O SKU continuará reservado e não poderá ser reutilizado.

**Critério de interface:** a ação visual “Excluir” executa somente a exclusão lógica, após confirmação; nenhum fluxo do MVP remove o arquivo canônico do produto.

### RF05 — Cadastro de movimentações
Permitir registrar movimentações dos tipos:
- ENTRADA;
- SAÍDA.

Cada movimentação deve conter:
- identificador único da movimentação;
- SKU do produto relacionado;
- tipo;
- quantidade inteira positiva;
- observação opcional;
- data/hora de criação;
- data/hora da última atualização;
- status de exclusão lógica.

### RF06 — Movimentação pela consulta de produto
Na tela/detalhe do produto, disponibilizar ações para registrar entrada ou saída já vinculadas ao produto selecionado.

### RF07 — Regras de estoque
Entradas aumentam o saldo e saídas diminuem o saldo. O sistema não pode permitir saldo negativo: uma saída maior que o saldo disponível deve ser rejeitada e apresentar mensagem compreensível. A quantidade deve ser informada como inteiro maior que zero. O saldo não pode ser alterado diretamente pelo formulário de produto.

### RF08 — Edição de movimentações
Permitir editar tipo, quantidade e observação de uma movimentação ativa. O produto relacionado (SKU) não poderá ser alterado. Para transferir uma movimentação para outro produto, o usuário deverá cancelar a movimentação original e criar outra.

A edição deve calcular o impacto líquido da alteração e validar que o saldo resultante não seja negativo.

### RF09 — Exclusão lógica de movimentações
Permitir cancelar uma movimentação por exclusão lógica, preservando o registro. O cancelamento deve reverter seu efeito no saldo. O cancelamento de uma entrada será bloqueado se sua reversão fizer o saldo ficar negativo.

### RF10 — Consulta de movimentações
Disponibilizar uma tela específica para consultar o histórico, com filtros mínimos:
- SKU;
- tipo (entrada/saída);
- período inicial e final;
- incluir movimentações canceladas.

Exibir identificador, data/hora, SKU, produto, tipo, quantidade e situação.

### RF11 — Dashboard
A tela principal deve apresentar:
- as 5 movimentações mais recentes não canceladas, sob o título “Últimas movimentações”;
- produtos ativos com saldo inferior a 5 unidades, incluindo saldo zero, sob o título “Produtos com saldo baixo”.

As informações devem refletir as movimentações registradas. Não haverá campo de estoque mínimo configurável nesta versão.

## 3. Requisitos não funcionais

### RNF01 — Interface gráfica
Todas as operações usuais devem ser realizadas por interface gráfica. O usuário final não deverá precisar operar o sistema pelo CMD ou terminal.

### RNF02 — Leveza e simplicidade
Priorizar interface limpa, direta e de baixo consumo de recursos. Utilizar Tkinter e ttk, evitando dependências visuais pesadas sem necessidade demonstrada.

### RNF03 — Persistência
Os dados devem permanecer disponíveis após fechar e reabrir a aplicação. Os arquivos JSON devem ser gravados com tratamento de erros e escrita segura.

### RNF04 — Separação de responsabilidades
Separar interface, casos de uso/regras de negócio, modelos e persistência. A interface não deve ler ou escrever JSON diretamente.

### RNF05 — Evolução da persistência
As regras de negócio não devem depender de detalhes de arquivos e caminhos. A implementação JSON deve ficar atrás de contratos/interfaces de repositório para facilitar futura substituição por banco de dados.

### RNF06 — Distribuição Windows
Entregar um executável Windows que inclua o interpretador Python e dependências necessárias, para que o usuário final não precise instalar Python. A geração do executável deverá ocorrer em ambiente Windows compatível.

### RNF07 — Execução pelo VS Code
Documentar como instalar Python, criar ambiente virtual, instalar dependências, executar testes e iniciar a aplicação pelo VS Code.

### RNF08 — Qualidade
Criar testes automatizados para regras de negócio e persistência, incluindo cenários de erro e integridade do saldo.

### RNF09 — Integridade e recuperação
Índices são estruturas auxiliares e reconstruíveis. Os registros canônicos são a fonte oficial. A aplicação deve detectar e reportar JSON inválido e oferecer estratégia segura de reconstrução de índices.

### RNF10 — Escopo de concorrência
A primeira versão destina-se a uso local por uma única instância/processo da aplicação. Não promete escrita simultânea multiusuário ou sincronização entre máquinas.

## 4. Restrições e premissas
- Linguagem: Python 3.11 ou superior, respeitando compatibilidade das dependências escolhidas.
- Interface: Tkinter + ttk.
- Persistência: JSON; não utilizar banco de dados nesta versão.
- Empacotamento: PyInstaller.
- Sistema-alvo do executável: Windows.
- Moeda: valores monetários tratados com `Decimal`; serialização JSON como strings decimais com duas casas.
- Datas: armazenar timestamps ISO 8601 com timezone UTC; exibir em horário local.
- Quantidade de estoque: inteiro positivo por movimentação.
- Sem autenticação, perfis, múltiplos depósitos, fornecedores, compras, vendas ou integração externa no MVP, salvo aprovação posterior.

## 5. Critérios de aceite iniciais
1. É possível cadastrar produto com SKU automático.
2. Tentativa de SKU duplicado é rejeitada, inclusive para produto excluído.
3. É possível editar dados permitidos sem alterar SKU ou saldo diretamente.
4. Produto pode ser excluído logicamente apenas com saldo zero.
5. Entrada aumenta saldo e saída diminui saldo.
6. Saída que gere saldo negativo é rejeitada.
7. Edição/cancelamento de movimentação atualiza saldo corretamente.
8. Dashboard mostra as 5 movimentações ativas mais recentes e produtos ativos com saldo < 5.
9. Fechar e reabrir a aplicação preserva dados.
10. Testes automatizados cobrem as regras críticas.
11. Aplicação inicia pelo VS Code seguindo a documentação.
12. Executável funciona em Windows sem Python instalado.

## 7. Ajustes planejados para a V2

Os itens abaixo são melhorias identificadas na revisão técnica da versão atual. Não alteram os requisitos nem o comportamento desta etapa e não devem ser considerados implementados pela geração do executável.

1. **Integridade dos índices de movimentação:** `by_product` é derivado, mas a consulta pode confiar nele e tratar índice ausente ou caminhos de registros inexistentes como ausência de movimentações. Validar/reconstruir o índice ou recorrer aos registros canônicos para que uma inconsistência não resulte em saldo incorreto.
2. **Validação dos registros JSON:** validar explicitamente os tipos de todos os campos durante a desserialização e converter dados inválidos em erro acionável com o caminho do arquivo.
3. **Isolamento das consultas do dashboard:** não deixar filtros aplicados na listagem de produtos alterarem o painel de baixo estoque.
4. **Tratamento de falhas de persistência na interface:** apresentar falhas de I/O ao usuário de forma compreensível, preservando a causa do erro.
5. **Escalabilidade das consultas:** evitar carregar e desserializar todo o histórico de movimentações em cada atualização da interface; avaliar consulta incremental/paginada ou índice recente, sem tornar índices fonte oficial dos dados.
6. **Manutenibilidade da apresentação:** melhorar formatação e tipagem da interface e, se necessário, separar montagem visual de callbacks, sem mover regras de negócio para a UI.

## 6. Itens fora do escopo inicial
- Banco de dados real.
- Operação multiusuário ou em rede.
- Controle por filial/depósito.
- Cadastro de fornecedores.
- Módulos de compras, vendas ou faturamento.
- Autenticação e permissões.
- Estoque mínimo configurável.
- Importação/exportação avançada, salvo necessidade identificada durante a implementação.
