# Prompt inicial para iniciar o trabalho no Codex

Leia integralmente todos os arquivos de `instructions/` e os documentos em `docs/` antes de implementar.

Você está no repositório do projeto Controle de Estoque. O baseline aprovado está documentado. Sua primeira tarefa é inspecionar a estrutura existente e confirmar se os documentos estão presentes, sem sobrescrever arquivos existentes sem antes entendê-los.

Em seguida:
1. Resuma brevemente o escopo e as decisões que entendeu.
2. Identifique conflitos ou bloqueios reais.
3. Apresente um plano incremental curto, compatível com o tempo recomendado de três horas.
4. **Comece a implementação pela Fase 1 — Fundação**, na mesma sessão, sem esperar nova autorização para decisões técnicas de baixo impacto.

Se encontrar uma lacuna que altere regra de negócio, escopo, experiência do usuário ou arquitetura aprovada, pare apenas a parte afetada e pergunte ao usuário. Não bloqueie o restante do trabalho por dúvidas que possam ser resolvidas com decisões técnicas simples e reversíveis.

Regras inegociáveis:
- Python + Tkinter/ttk.
- JSON como persistência inicial; não introduzir banco de dados.
- Interface gráfica; não criar fluxo principal de terminal.
- UI não acessa JSON diretamente.
- SKU manual ou automático, único, normalizado e reservado após soft delete.
- Movimentações ativas são a fonte oficial do saldo.
- Nunca permitir estoque negativo.
- Produtos e movimentações usam exclusão lógica.
- Índices e saldo cacheado são reconstruíveis/derivados.
- Documentar alterações e uso de IA com transparência.
- Não alterar requisitos ou decisões sem aprovação do usuário.

Se precisar escolher detalhe técnico de baixo impacto, adote a opção mais simples, mantenha boas práticas e registre a decisão. Se a escolha mudar regra de negócio, escopo, experiência do usuário ou arquitetura aprovada, pergunte antes.

Implemente em incrementos pequenos. Ao concluir cada fase, execute testes e informe resultados reais. Nunca declare testes como aprovados sem executá-los.

Ao terminar a Fase 1, apresente arquivos criados/alterados, comandos de execução, testes realizados e próximo incremento recomendado. Continue para as fases seguintes conforme a capacidade da sessão e o tempo disponível, sem sacrificar integridade do estoque ou testes críticos.
