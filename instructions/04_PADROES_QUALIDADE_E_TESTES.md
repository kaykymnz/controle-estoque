# Padrões de implementação, qualidade e testes

## Código

- Usar type hints nas interfaces públicas e funções relevantes.
- Nomes claros e consistentes.
- Funções curtas com uma responsabilidade.
- Evitar duplicação de lógica e validações.
- Centralizar regras de estoque em serviço de domínio/aplicação, nunca replicar em telas.
- Tratar exceções específicas; não usar `except: pass`.
- Separar configuração de caminhos e dados.
- Evitar dependências externas sem necessidade.
- Não adicionar framework de injeção de dependência; composição explícita na inicialização é suficiente.
- Não usar `eval` ou desserialização insegura.
- Não armazenar preços como float.

## Interface

- Usar Tkinter + ttk.
- Interface limpa, consistente e de baixa complexidade visual.
- Utilizar diálogos de confirmação para exclusão/cancelamento.
- Mostrar mensagens de validação compreensíveis em português.
- Não congelar a janela em operações demoradas; para o volume esperado, manter operações simples e responsivas.
- Não misturar regra de negócio com callbacks.
- Não usar terminal para a operação normal do usuário.

## Testes mínimos

### Produtos
- criar com SKU automático;
- normalização de SKU;
- rejeitar SKU duplicado;
- SKU continua reservado após soft delete;
- editar campos permitidos;
- rejeitar edição de SKU/saldo;
- bloquear exclusão com saldo positivo;
- permitir exclusão com saldo zero.

### Movimentações
- entrada aumenta saldo;
- saída reduz saldo;
- saída acima do saldo é rejeitada;
- quantidade zero, negativa ou fracionária é rejeitada;
- editar entrada/saída recalcula corretamente;
- cancelar saída devolve quantidade;
- cancelar entrada é bloqueado quando deixaria saldo negativo;
- movimentação cancelada não compõe saldo;
- produto excluído não aceita nova movimentação.

### Persistência
- dados permanecem após reconstruir repositórios/reiniciar serviços;
- gravação temporária e substituição;
- índice SKU é reconstruível;
- índice por produto é reconstruível;
- saldo cacheado é reconciliável;
- JSON inválido gera erro tratado e mensagem acionável.

## Ferramentas

- Usar `unittest` ou `pytest`; escolher uma única opção e documentar.
- Testes de persistência devem usar diretórios temporários isolados.
- Não depender de dados reais em `data/`.
- Executar todos os testes antes de declarar etapa concluída.

## Critérios de conclusão por etapa

Uma etapa só está concluída quando:
1. implementação existe;
2. testes relevantes passam;
3. comportamento manual básico foi verificado quando aplicável;
4. documentação foi atualizada;
5. limitações conhecidas foram reportadas.
