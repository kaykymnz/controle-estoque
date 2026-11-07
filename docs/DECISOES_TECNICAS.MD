# Decisões Técnicas

## DT001 — Identificação de produtos por SKU

**Contexto:**

O sistema precisa garantir que cada produto possua um identificador único, evitando duplicidade de cadastros.

**Decisão:**

Utilizar o SKU como identificador principal dos produtos, substituindo o conceito genérico de ID.

**Justificativa:**

O SKU permitirá identificar individualmente cada produto e estabelecer relacionamentos com as movimentações de estoque.

O identificador deverá ser único e imutável após o cadastro.

## DT002 — Separação dos registros e índices

**Contexto:**

A utilização de um único arquivo JSON contendo todos os produtos poderia tornar operações individuais menos eficientes, além de dificultar a manutenção dos dados.

**Decisão:**

Armazenar cada produto em um arquivo JSON individual e manter índices separados para localização e controle de identificadores.

**Estratégia proposta:**

- Cada produto terá seu próprio arquivo JSON.
- Os SKUs serão armazenados em arquivos exclusivos de registro de identificadores.
- O índice de SKUs será dividido em grupos utilizando hash SHA-256.
- Cada consulta de duplicidade deverá acessar somente o grupo correspondente ao SKU pesquisado.
- Os índices serão considerados estruturas auxiliares, podendo ser reconstruídos a partir dos registros oficiais.

**Justificativa:**

Reduzir a necessidade de leitura de grandes arquivos, melhorar a organização e facilitar a evolução da persistência.

## DT003 — Exclusão lógica de produtos

**Contexto:**

A exclusão definitiva de produtos poderia comprometer o histórico de movimentações e relacionamentos.

**Decisão:**

Implementar exclusão lógica por meio de um indicador de status.

**Justificativa:**

Preservar os registros históricos e impedir a reutilização de SKUs anteriormente cadastrados.

## DT004 — Separação da camada de persistência

**Contexto:**

A aplicação utilizará JSON inicialmente, mas deverá permitir integração futura com banco de dados.

**Decisão:**

Isolar o acesso aos arquivos JSON em uma camada específica de persistência.

**Justificativa:**

Evitar dependência direta entre regras de negócio, interface gráfica e tecnologia de armazenamento.

## DT005 — Integridade dos arquivos

**Contexto:**

Arquivos JSON não oferecem mecanismos transacionais equivalentes aos encontrados em bancos de dados.

**Decisão:**

Adotar mecanismos de gravação segura, operações controladas e verificação de consistência entre registros e índices.

**Justificativa:**

Reduzir o risco de corrupção e inconsistência dos dados durante operações que envolvam múltiplos arquivos.

## DT006 — Controle de quantidade em estoque

**Contexto:**

A quantidade disponível não deverá ser alterada diretamente durante o cadastro ou edição de produtos.

**Decisão:**

O estoque será controlado por meio de movimentações de entrada e saída.

**Justificativa:**

Manter a rastreabilidade das alterações e evitar divergências entre o estoque disponível e o histórico de movimentações.

---

## DT007 — Estratégia de identificação por SKU

**Contexto:**

O sistema precisa permitir que o usuário informe seu próprio SKU ou utilize um identificador gerado automaticamente.

**Decisão:**

O sistema oferecerá duas modalidades de identificação:

- SKU informado manualmente pelo usuário.
- SKU gerado automaticamente pelo sistema.

O formato será alfanumérico, permitindo letras, números e separadores previamente definidos.

**Regras:**

- Os identificadores serão normalizados para letras maiúsculas.
- Espaços externos serão removidos.
- A unicidade será obrigatória.
- SKUs já utilizados não poderão ser reutilizados, inclusive após exclusão lógica.
- O SKU não poderá ser alterado pela edição convencional do produto.

**Justificativa:**

Oferecer flexibilidade para diferentes operações comerciais, mantendo a identificação única e consistente dos produtos.

## DT008 — Identificação física dos arquivos

**Decisão:**

Os nomes físicos dos arquivos de produtos não dependerão diretamente do SKU informado.

Será utilizada uma identificação derivada por hash, evitando problemas com caracteres especiais, caminhos inválidos e nomes de arquivos.

O SKU original normalizado permanecerá armazenado no conteúdo do registro.

**Justificativa:**

Separar a identificação de negócio da identificação física utilizada pela persistência.