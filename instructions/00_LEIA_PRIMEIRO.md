# Instruções para o Codex — Leia antes de implementar

Você está trabalhando no projeto **Controle de Estoque**, uma aplicação desktop em Python.

## Regra principal

Antes de escrever ou alterar código:
1. Leia todos os arquivos desta pasta `instructions/`.
2. Leia `docs/REQUISITOS.md`.
3. Leia `docs/DECISOES_TECNICAS.md`.
4. Leia `docs/ARQUITETURA_E_DADOS.md`.
5. Leia `docs/HISTORICO_DESENVOLVIMENTO.md`.

Esses documentos formam o baseline aprovado pelo usuário.

## Papel do Codex

Você será responsável por gerar e modificar o código, propor uma sequência de implementação, executar testes e reportar resultados. O usuário é responsável pelas decisões de produto e aprovação das mudanças de escopo.

Não alegue que o usuário escreveu manualmente código gerado por IA. A documentação deve ser transparente sobre o uso de IA.

## Não inventar regras

- Não alterar requisitos ou decisões técnicas por conta própria.
- Se encontrar ambiguidade, conflito ou requisito inviável, explique o problema e pergunte ao usuário antes de mudar o baseline.
- Melhorias internas pequenas que não alterem comportamento podem seguir boas práticas, mas devem ser explicadas.
- Não adicionar funcionalidades fora do escopo para "sofisticar" o projeto.
- Não substituir JSON por banco de dados.
- Não criar uma aplicação de terminal; o fluxo de uso deve ser gráfico.

## Prioridade

O desafio tem tempo recomendado de até três horas. Priorize um MVP funcional, simples, testável e bem documentado. Evite arquitetura excessiva, dependências desnecessárias e abstrações sem uso.

## Ao concluir cada etapa

Informe:
- arquivos criados/alterados;
- comportamento implementado;
- decisões tomadas;
- testes executados e resultados;
- limitações ou riscos conhecidos;
- documentos que precisam ser atualizados.

Atualize `docs/HISTORICO_DESENVOLVIMENTO.md` e os documentos técnicos pertinentes. Não apague o histórico anterior.
