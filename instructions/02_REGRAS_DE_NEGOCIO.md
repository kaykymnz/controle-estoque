# Regras de negócio obrigatórias

## Produtos

- SKU obrigatório, único e normalizado para maiúsculas; remover espaços externos.
- SKU sempre automático; não aceitar preenchimento manual.
- SKU automático no formato `PRD-XXXXXXXX`, oito caracteres hexadecimais maiúsculos derivados de UUID; consultar índice e repetir geração se houver colisão.
- SKU não pode ser alterado na edição convencional.
- Nome obrigatório.
- Descrição e categoria opcionais; categoria é texto livre.
- Preços de custo e venda opcionais e não negativos; usar `Decimal`.
- Não aceitar estoque informado no formulário de produto.
- Saldo inicial é zero e saldo só muda por movimentações.
- Exclusão é lógica; SKU não é liberado.
- Bloquear exclusão de produto com saldo diferente de zero.
- Produto excluído não aceita movimentações novas.

## Movimentações

- Tipos: `ENTRY` e `EXIT`.
- Quantidade deve ser inteiro positivo.
- SKU deve referenciar produto existente e ativo.
- Entrada soma quantidade; saída subtrai quantidade.
- Saldo nunca pode ficar negativo.
- Movimentação pode ser editada nos campos tipo, quantidade e observação.
- SKU de uma movimentação não pode ser alterado na edição.
- Para mudar o produto relacionado, cancelar a movimentação anterior e criar outra.
- Exclusão é lógica/cancelamento; não apagar arquivo.
- Cancelar ENTRY subtrai seu efeito. Se resultar em saldo negativo, bloquear cancelamento.
- Cancelar EXIT soma novamente a quantidade ao saldo.
- Editar movimento deve calcular o efeito antigo e o novo: saldo resultante = saldo atual - efeito antigo + efeito novo. Rejeitar se negativo.
- Movimentações canceladas permanecem consultáveis quando o filtro correspondente estiver habilitado.

## Estoque

Saldo oficial calculado:
`sum(ENTRY ativos) - sum(EXIT ativos)`

O campo `current_stock` no produto é cache derivado, não fonte oficial. Criar serviço de reconciliação para recalcular o cache com base no histórico ativo.

## Dashboard

- Mostrar as 5 movimentações mais recentes não canceladas.
- Mostrar produtos ativos com saldo estritamente inferior a 5; inclui zero.
- Não existe configuração de estoque mínimo por produto.

## Consultas

Produtos: filtros por SKU, nome, categoria, situação do estoque (todos/zerado/positivo) e opção para incluir excluídos.

Movimentações: filtros por SKU, tipo, data inicial/final e opção para incluir canceladas.

## Datas e dinheiro

- Persistir timestamps ISO 8601 com timezone UTC.
- Exibir datas em horário local.
- Valores monetários calculados com `Decimal`.
- Serializar preços como strings com duas casas decimais, por exemplo `"19.90"`.
