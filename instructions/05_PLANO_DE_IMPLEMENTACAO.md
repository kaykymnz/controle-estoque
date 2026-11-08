# Plano de implementação sugerido

Implementar em incrementos pequenos e verificáveis. Não tentar gerar toda a aplicação em uma única alteração.

## Fase 0 — Inspeção
- Inspecionar repositório e arquivos existentes.
- Ler todas as instruções e documentos.
- Não sobrescrever README, estrutura ou arquivos existentes sem inspecionar.
- Apresentar plano curto de execução e dependências.

## Fase 1 — Fundação
- Criar estrutura mínima de pacotes.
- Configurar inicialização e resolução do diretório de dados.
- Definir modelos, enums, exceções e contratos de repositório.
- Criar testes básicos e configuração de execução.
- Validar que a aplicação abre uma janela Tkinter.

## Fase 2 — Persistência JSON
- Implementar leitura/escrita segura.
- Implementar repositório de produtos e índice SKU.
- Implementar repositório de movimentações e índices necessários.
- Implementar reconstrução de índices e reconciliação de saldos.
- Testar com diretório temporário.

## Fase 3 — Regras de negócio
- Serviço de produtos.
- Serviço de movimentações.
- Cálculo de saldo e validação de saldo negativo.
- Edição e cancelamento lógico de movimentações.
- Testes unitários completos das regras críticas.

## Fase 4 — Interface
- Janela principal e navegação.
- Dashboard.
- Listagem/filtros de produtos.
- Formulário de cadastro/edição de produto.
- Detalhe do produto com ações de entrada/saída.
- Consulta e edição/cancelamento de movimentações.
- Mensagens de erro/sucesso em português.
- Manter UI simples e consistente.

## Fase 5 — Integração e validação
- Testar fluxo completo: cadastrar → entrada → saída → consultar → editar/cancelar → conferir saldo.
- Testar persistência após fechar e abrir.
- Testar exclusão lógica.
- Testar dados inválidos e erros de arquivo.
- Atualizar README e documentação.

## Fase 6 — Distribuição
- Configurar PyInstaller com `--onefile --windowed`.
- Definir nome e ícone se houver asset aprovado.
- Confirmar que dados são gravados em `%LOCALAPPDATA%`.
- Gerar executável em Windows.
- Testar em máquina/ambiente Windows sem Python instalado, quando possível.
- Publicar binário em GitHub Releases e incluir link destacado no README.

## Gestão do tempo

Priorizar um MVP funcional. Se o tempo apertar, não sacrificar regras de integridade ou testes do saldo para adicionar efeitos visuais. O mínimo indispensável é cadastro, consulta, entrada/saída, histórico, dashboard, persistência e execução.
