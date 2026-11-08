# Arquitetura e persistência — instruções para implementação

## Camadas

Manter separação clara:
- Domain: entidades, enums, exceções e regras centrais.
- Application: serviços/casos de uso e contratos de repositório.
- Infrastructure: repositórios JSON, serialização, índices e resolução de caminhos.
- Presentation: telas, widgets, diálogos e eventos Tkinter.
- App: inicialização e configuração.

A UI não acessa arquivos JSON diretamente. Nenhuma regra de negócio deve ficar dentro de callbacks de widgets.

## Persistência

Usar registros individuais:
- Produto: arquivo individual derivado do SHA-256 do SKU normalizado.
- Movimentação: arquivo individual com ID `MOV-<UUID>`, organizado por ano/mês da criação.
- SKU registry: shards por prefixo dos dois primeiros caracteres hexadecimais do SHA-256 do SKU. Mapa SKU normalizado → identificador/caminho do registro.
- Índice por produto para localizar movimentações.
- Índice recente limitado para apoiar dashboard, se necessário.

Criar shards e índices sob demanda; não criar todos vazios na inicialização.

## Fonte oficial e índices

- Registros individuais são a fonte oficial.
- Índices são derivados, auxiliares e reconstruíveis.
- Cache `current_stock` é derivado do histórico ativo.
- Implementar rotina de verificação/reconstrução de índices e reconciliação de saldos.
- Não tratar o índice como verdade definitiva; validar o SKU completo no registro.

## Segurança de gravação

- Serializar JSON de forma consistente (UTF-8, indentação legível).
- Escrever primeiro em arquivo temporário no mesmo diretório.
- Substituir destino com `os.replace` quando suportado.
- Tratar exceções de I/O e não ocultar falhas.
- Não deixar arquivo parcial como se fosse válido.
- Em falhas entre gravações de movimento e cache do produto, reconciliar cache a partir do ledger canônico.
- Não prometer transações ACID ou multiusuário.

## Caminhos de dados

- Desenvolvimento: `data/` na raiz do projeto.
- Executável Windows: `%LOCALAPPDATA%/ControleEstoque/data`.
- Não escrever dados operacionais na pasta do executável ou no diretório temporário do PyInstaller.
- Criar diretórios automaticamente quando necessário.

## Estrutura sugerida

Consulte `docs/ARQUITETURA_E_DADOS.md`. Adapte sem criar camadas ou classes vazias. O projeto deve continuar pequeno e compreensível.
