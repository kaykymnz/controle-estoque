# Arquitetura e Organização dos Dados

## 1. Objetivo arquitetural

Manter uma aplicação desktop pequena, organizada e testável, com separação entre interface, regras de negócio e persistência. O armazenamento inicial é JSON, mas a lógica central não deve conhecer detalhes de arquivos.

## 2. Organização de código sugerida

```text
src/
└── controle_estoque/
    ├── main.py
    ├── app/
    │   ├── config.py
    │   └── paths.py
    ├── domain/
    │   ├── models/
    │   ├── enums/
    │   └── exceptions.py
    ├── application/
    │   ├── services/
    │   └── interfaces/
    ├── infrastructure/
    │   └── persistence/
    │       └── json/
    │           ├── repositories/
    │           ├── indexes/
    │           └── serializers.py
    └── presentation/
        └── ui/
            ├── windows/
            ├── views/
            ├── dialogs/
            └── components/
tests/
data/
docs/
instructions/
```

A estrutura é uma orientação, não uma obrigação de criar abstrações vazias. Manter o projeto simples e proporcional ao desafio.

## 3. Dependências entre camadas

- `presentation`: widgets, telas, formulários e interação. Chama serviços/casos de uso; não acessa arquivos.
- `application`: orquestra casos de uso e valida regras operacionais; depende de interfaces de repositório.
- `domain`: modelos, enums, validações centrais e regras independentes de UI/JSON.
- `infrastructure`: implementa repositórios e serialização JSON.
- `app`: configuração, inicialização e resolução do diretório de dados.

Direção desejada: apresentação → aplicação → domínio; infraestrutura implementa contratos utilizados pela aplicação. Evitar dependências da camada de domínio em Tkinter ou em caminhos de arquivos.

## 4. Diretório de dados

Em desenvolvimento, utilizar `data/` no projeto (ignorado pelo Git para dados gerados pelo usuário, mantendo opcionalmente arquivos de exemplo vazios/documentados).

Na versão empacotada Windows, usar:
`%LOCALAPPDATA%/ControleEstoque/data`

Nunca gravar dados operacionais dentro da pasta temporária do PyInstaller ou depender de escrita ao lado do executável.

## 5. Estrutura lógica de dados

```text
data/
├── products/
│   ├── records/
│   │   ├── 0a/
│   │   │   └── <sha256-do-sku>.json
│   │   └── ...
│   └── indexes/
│       └── sku_registry/
│           ├── 0a.json
│           ├── 1b.json
│           └── ...
├── movements/
│   ├── records/
│   │   └── YYYY/
│   │       └── MM/
│   │           └── MOV-<uuid>.json
│   └── indexes/
│       ├── by_product/
│       │   └── <prefixo-hash>.json
│       └── recent.json
├── metadata/
│   └── schema.json
└── backups/
```

Os arquivos e índices devem ser criados sob demanda. Não criar centenas de arquivos vazios na inicialização.

## 6. Produto — modelo lógico

```json
{
  "sku": "PRD-00A1B2C3",
  "name": "Teclado Mecânico",
  "description": "Teclado mecânico ABNT2",
  "category": "Periféricos",
  "cost_price": "120.00",
  "sale_price": "189.90",
  "current_stock": 12,
  "created_at": "2026-11-07T18:00:00+00:00",
  "updated_at": "2026-11-07T18:00:00+00:00",
  "is_deleted": false,
  "deleted_at": null
}
```

Observações:
- Exemplo ilustrativo, não dado real.
- Preços são strings decimais para preservar precisão.
- `current_stock` é cache derivado das movimentações ativas e não pode ser editado pelo usuário.
- SKU é armazenado normalizado.
- `deleted_at` fica preenchido quando houver exclusão lógica.

## 7. Movimentação — modelo lógico

```json
{
  "movement_id": "MOV-<UUID>",
  "sku": "PRD-00A1B2C3",
  "type": "ENTRY",
  "quantity": 5,
  "note": "Reposição",
  "created_at": "2026-11-07T18:10:00+00:00",
  "updated_at": "2026-11-07T18:10:00+00:00",
  "is_deleted": false,
  "deleted_at": null
}
```

`type` aceita `ENTRY` ou `EXIT`. Quantidade é inteiro positivo. SKU referencia o produto e não muda em uma edição.

## 8. Registro de SKUs

O índice de SKU é particionado por prefixo dos primeiros dois caracteres hexadecimais do SHA-256 do SKU normalizado. Cada arquivo guarda um mapa SKU → identificador/caminho do registro. A verificação consulta somente o shard correspondente.

O registro de SKUs inclui também produtos excluídos logicamente. O índice é reconstruível a partir dos registros de produtos.

Não confiar apenas no hash: validar o SKU completo encontrado no registro.

## 9. Movimentações e índices

Movimentações são registros individuais. O caminho por ano/mês usa `created_at` e não deve mudar quando a movimentação é editada. O índice `by_product` permite recuperar movimentações de um SKU. `recent.json` pode manter uma janela limitada das movimentações mais recentes para o dashboard.

Todos os índices são derivados e reconstruíveis. O histórico canônico está nos arquivos individuais de movimentação.

## 10. Saldo e reconciliação

Saldo de um produto:
`saldo = soma(quantidades de ENTRY ativos) - soma(quantidades de EXIT ativos)`

`current_stock` é cache. Após falha ou divergência, serviço de reconciliação recalcula o saldo com base nas movimentações ativas e atualiza o produto.

Ao criar/editar/cancelar movimentação, validar o saldo resultante antes de confirmar a alteração. Gravar arquivos com escrita temporária e `os.replace` quando suportado.

## 11. Limitações conhecidas

- JSON não oferece transações ACID.
- MVP não suporta gravações simultâneas multiusuário.
- Índices e caches precisam de verificação/reconstrução.
- Para escala ou uso multiusuário, migrar para banco de dados; não tentar transformar JSON em banco completo.
