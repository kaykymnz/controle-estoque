# Documentação, transparência e entrega

## Documentos que devem permanecer atualizados

- `README.md`: visão geral, funcionalidades, tecnologias, execução, testes e download do executável.
- `docs/REQUISITOS.md`: requisitos e critérios de aceite.
- `docs/DECISOES_TECNICAS.md`: decisões, contexto e justificativas.
- `docs/HISTORICO_DESENVOLVIMENTO.md`: solicitações, atividades da IA, dúvidas, respostas e validações.
- `docs/ARQUITETURA_E_DADOS.md`: arquitetura, modelos e armazenamento.
- `instructions/`: contexto e regras de implementação para o Codex.

## Registro de trabalho com IA

Ao concluir cada incremento, registrar no histórico:
- solicitação do usuário;
- atividade executada pelo Codex/IA;
- dúvidas apresentadas;
- resposta/decisão do usuário;
- validação e testes;
- arquivos/documentos atualizados.

Não inventar perguntas/respostas que não ocorreram. Não registrar uma decisão como aprovada sem confirmação do usuário quando ela alterar comportamento ou escopo.

## README final

Deve conter:
- descrição objetiva;
- funcionalidades;
- tecnologias;
- capturas de tela, se disponíveis;
- link para baixar executável Windows;
- instruções para executar pelo VS Code;
- como executar testes;
- localização dos dados;
- limitações conhecidas;
- informação transparente sobre uso de IA.

## Execução pelo VS Code

Documentar:
1. instalar versão compatível do Python;
2. clonar repositório;
3. abrir pasta no VS Code;
4. criar ambiente virtual;
5. ativar ambiente;
6. instalar dependências;
7. iniciar a aplicação;
8. executar testes.

Fornecer comandos específicos para Windows PowerShell e, se simples, alternativas para macOS/Linux. Não exigir essas plataformas para o executável Windows.

## Executável

- Gerar com PyInstaller em Windows.
- Usar modo sem console para a aplicação gráfica.
- Dados ficam fora do executável, em diretório gravável do usuário.
- Testar o binário em Windows sem Python instalado.
- Preferir anexar o executável a uma GitHub Release e colocar link claro no README; não versionar grandes binários de build no histórico Git sem necessidade.
- Manter configuração, dependências, automação do PyInstaller, ambiente virtual, intermediários e executável em `dir_exe/`; ignorar toda essa pasta no Git.
- Publicar o executável como anexo de uma GitHub Release, não como commit nem arquivo rastreado no repositório.
- Documentar com clareza a diferença entre build local e release publicada. Não afirmar compatibilidade sem teste do executável em Windows sem Python instalado.

## Relato final

Ao terminar, apresentar:
- o que foi implementado;
- como executar;
- como testar;
- onde está o executável;
- quais testes passaram;
- limitações e próximos passos.
