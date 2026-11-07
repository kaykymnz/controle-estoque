# Requisitos do Sistema — Controle de Estoque

**Projeto:** Controle de Estoque  
**Linguagem:** Python  
**Tipo de aplicação:** Desktop com interface gráfica  
**Persistência:** Arquivos JSON  
**Status:** Em levantamento e validação

---

# 1. Visão geral

O projeto consiste no desenvolvimento de um sistema desktop para gerenciamento e controle de estoque, permitindo o cadastro e gerenciamento de produtos, registro de movimentações, consulta de disponibilidade e acompanhamento das operações por meio de um dashboard.

A aplicação será desenvolvida em Python, utilizando uma interface gráfica para interação com o usuário.

Embora a persistência inicial seja realizada por arquivos JSON, a estrutura interna será planejada para permitir uma futura substituição por um banco de dados, sem exigir alterações significativas nas regras de negócio.

# 2. Requisitos funcionais

## RF01 — Gerenciamento de produtos

O sistema deverá permitir:

- Cadastrar novos produtos.
- Editar informações de produtos existentes.
- Consultar produtos cadastrados.
- Excluir produtos por meio de exclusão lógica (*soft delete*).

A exclusão lógica deverá preservar os registros no armazenamento, evitando a remoção definitiva dos dados.

Produtos excluídos não deverão aparecer nas consultas convencionais, salvo quando houver um filtro específico para essa finalidade.

## RF02 — Consulta de estoque

O sistema deverá permitir consultar a quantidade disponível de produtos em estoque.

A consulta deverá oferecer filtros para personalizar os resultados apresentados, permitindo que o usuário escolha quais informações deseja visualizar.

Os filtros e campos disponíveis serão detalhados durante o refinamento dos requisitos.

## RF03 — Gerenciamento de movimentações

O sistema deverá permitir o gerenciamento das movimentações de estoque, contemplando:

- Registro de novas movimentações.
- Consulta de movimentações existentes.
- Edição de movimentações.
- Exclusão de movimentações.

As movimentações deverão representar operações que alteram a quantidade disponível de produtos em estoque.

## RF04 — Movimentação diretamente pela consulta de produtos

Ao consultar um produto, o sistema deverá disponibilizar ações para registrar diretamente uma movimentação de estoque.

O usuário deverá conseguir:

- Registrar uma entrada de produtos.
- Registrar uma saída de produtos.

A operação deverá estar vinculada ao produto consultado, evitando a necessidade de realizar uma nova seleção manual do produto.

## RF05 — Persistência em arquivos JSON

Nesta primeira versão, o sistema não utilizará um banco de dados.

Os dados serão armazenados em arquivos no formato JSON, permitindo a persistência das informações entre as execuções da aplicação.

**Justificativa:** A utilização de arquivos JSON atende à proposta de um desafio prático, reduzindo a complexidade de configuração e infraestrutura, sem comprometer a possibilidade de evolução futura.

## RF06 — Estrutura preparada para banco de dados

Apesar da utilização de arquivos JSON, a arquitetura deverá considerar uma futura integração com banco de dados.

As regras de negócio não deverão depender diretamente da tecnologia de armazenamento.

Deverá existir uma separação entre:

- Regras de negócio.
- Camada responsável pelo acesso e persistência dos dados.
- Interface gráfica.

Na implementação inicial, as operações de persistência serão realizadas por meio de arquivos JSON.

Em uma evolução futura, essa camada poderá ser substituída por uma implementação de banco de dados, preservando, sempre que possível, as demais partes da aplicação.

## RF07 — Dashboard principal

A tela inicial deverá apresentar um dashboard com informações relevantes sobre o estoque.

O dashboard deverá conter:

- Últimas movimentações realizadas.
- Produtos com quantidade disponível inferior a 5 unidades.

As informações deverão ser atualizadas de acordo com as movimentações registradas no sistema.

## RF08 — Consulta de movimentações

O sistema deverá disponibilizar uma tela ou seção específica para consulta do histórico de movimentações.

O usuário deverá conseguir visualizar as movimentações registradas, permitindo acompanhar as operações realizadas no estoque.

Os critérios de filtragem e as informações apresentadas serão detalhados posteriormente.

---

# 3. Requisitos não funcionais

## RNF01 — Interface gráfica

A aplicação deverá possuir uma interface gráfica desktop, permitindo que todas as operações sejam realizadas visualmente.

Não deverá ser necessário utilizar o terminal ou CMD para operar o sistema no uso convencional.

## RNF02 — Persistência de dados

Os dados deverão permanecer disponíveis após o encerramento e a reabertura da aplicação.

A persistência deverá ser realizada por arquivos JSON durante a versão inicial.

## RNF03 — Arquitetura preparada para evolução

A estrutura do software deverá permitir a substituição da persistência JSON por um banco de dados no futuro, minimizando o acoplamento entre as regras de negócio e a camada de armazenamento.

## RNF04 — Distribuição executável

O projeto deverá disponibilizar uma versão executável no formato `.exe`, permitindo que usuários executem a aplicação em máquinas Windows sem a necessidade de instalar Python ou configurar o ambiente de desenvolvimento.

O executável deverá ser disponibilizado na área principal do repositório ou por meio de uma publicação de versão no GitHub.

## RNF05 — Ambiente de desenvolvimento

O projeto também deverá permitir sua execução em ambiente de desenvolvimento utilizando Visual Studio Code.

Deverá existir documentação específica explicando:

- Pré-requisitos para execução.
- Instalação do Python.
- Configuração do ambiente virtual.
- Instalação das dependências.
- Organização dos arquivos.
- Como iniciar a aplicação pelo VS Code.

## RNF06 — Manutenibilidade

O código deverá ser organizado em módulos com responsabilidades bem definidas, priorizando:

- Separação de responsabilidades.
- Reutilização de código.
- Baixo acoplamento.
- Facilidade de manutenção.
- Evitar duplicidade de implementações.

## RNF07 — Integridade dos dados

As operações realizadas deverão preservar a consistência das informações armazenadas.

Alterações em produtos e movimentações deverão refletir corretamente na quantidade disponível em estoque.

## RNF08 — Documentação

O projeto deverá possuir documentação suficiente para explicar seu funcionamento, suas decisões técnicas, sua estrutura e suas formas de execução.

---

# 4. Restrições e decisões iniciais

| Item | Definição |
|---|---|
| Linguagem | Python |
| Interface | Aplicação gráfica desktop |
| Persistência inicial | Arquivos JSON |
| Banco de dados | Não será utilizado nesta versão |
| Arquitetura | Preparada para futura integração com banco de dados |
| Distribuição | Executável Windows `.exe` |
| Ambiente de desenvolvimento | Visual Studio Code |
| Interface de operação | Gráfica, sem dependência do CMD |

# 5. Itens pendentes de definição

Os seguintes pontos ainda precisam ser discutidos e aprovados:

- Campos obrigatórios no cadastro de produtos.
- Critérios e opções de filtragem de produtos.
- Informações obrigatórias em uma movimentação.
- Regras para edição e exclusão de movimentações.
- Validações para entradas e saídas.
- Critérios de filtragem do histórico.
- Comportamento de produtos excluídos.
- Tecnologias e bibliotecas para interface gráfica.
- Estratégia de armazenamento e organização dos arquivos JSON.

---

**Observação:** Este documento representa a primeira versão dos requisitos. Novas definições serão incorporadas conforme o levantamento avançar.