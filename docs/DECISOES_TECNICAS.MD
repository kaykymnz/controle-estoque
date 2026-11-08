# Decisões Técnicas — Controle de Estoque

Este documento registra decisões aprovadas e suas justificativas. Mudanças posteriores devem ser registradas com contexto, impacto e aprovação do responsável pelo produto.

## DT001 — Linguagem Python
**Decisão:** utilizar Python.  
**Justificativa:** linguagem permitida no desafio, produtiva para um MVP e adequada ao desenvolvimento desktop com persistência JSON.

## DT002 — Aplicação desktop gráfica
**Decisão:** desenvolver aplicação desktop, sem fluxo operacional dependente do terminal.  
**Justificativa:** o usuário final deve operar visualmente e o desafio pede uma solução utilizável.

## DT003 — Tkinter + ttk
**Decisão:** utilizar Tkinter e widgets ttk para a interface.  
**Justificativa:** solução incluída na distribuição padrão do Python, leve e suficiente para formulários, tabelas, navegação e dashboard simples. Evitar framework visual pesado no escopo de três horas. Manter componentes visuais desacoplados das regras de negócio.

## DT004 — Persistência JSON na primeira versão
**Decisão:** não utilizar banco de dados no MVP.  
**Justificativa:** reduzir infraestrutura e tempo de configuração no desafio prático. A limitação de concorrência e transações deve ser explicitada.

## DT005 — Camada de persistência isolada
**Decisão:** regras de negócio não acessam arquivos diretamente. A aplicação utiliza contratos de repositório e uma implementação JSON.  
**Justificativa:** permitir substituir JSON por SQLite ou outro banco futuramente sem reescrever a interface e as regras centrais.

## DT006 — Um arquivo por registro
**Decisão:** armazenar cada produto e cada movimentação em arquivo individual.  
**Justificativa:** evitar regravação de um único JSON grande para atualizações individuais e facilitar localização e recuperação.

## DT007 — SKU como identificador de negócio
**Decisão:** SKU é o identificador único do produto. A modalidade manual foi substituída pela DT025; o SKU é sempre automático.
**Regras:** normalizar para maiúsculas e remover espaços externos; aceitar formato alfanumérico com separadores permitidos; SKU imutável na edição convencional; SKU não é liberado após exclusão lógica.

## DT008 — SKU automático
**Decisão:** gerar SKU no formato `PRD-XXXXXXXX`, em que `XXXXXXXX` são oito caracteres hexadecimais maiúsculos derivados de UUID aleatório. Verificar unicidade no registro de SKUs antes de confirmar. Em colisão, gerar outro identificador.  
**Justificativa:** formato legível, sem contador global e com probabilidade extremamente baixa de colisão.

## DT009 — Arquivos e índices particionados por hash
**Decisão:** derivar um identificador físico determinístico do SKU normalizado usando SHA-256. Guardar registros em subpastas pelo prefixo do hash. Manter registro de SKUs particionado pelo mesmo prefixo de hash.  
**Justificativa:** não usar entrada do usuário diretamente em caminhos; evitar um único índice gigantesco. O índice é auxiliar e reconstruível a partir dos registros canônicos. Em colisão de hash, comparar o SKU completo armazenado e não assumir igualdade apenas pelo hash.

## DT010 — Índices reconstruíveis
**Decisão:** índices não são fonte oficial dos dados. Devem poder ser reconstruídos a partir dos registros canônicos.  
**Justificativa:** recuperação de inconsistências e prevenção de divergência permanente.

## DT011 — Exclusão lógica de produtos
**Decisão:** produtos não são apagados fisicamente. Marcar `is_deleted=true` e registrar `deleted_at`. SKU permanece reservado. Não permitir excluir produto com saldo diferente de zero.  
**Justificativa:** preservar histórico e impedir que movimentações antigas apontem para um identificador reutilizado.

## DT012 — Estoque derivado de movimentações
**Decisão:** movimentações ativas são a fonte oficial do saldo. Saldo atual no produto é cache/projeção para consulta, nunca editável diretamente.  
**Regra:** saldo = soma das entradas ativas menos soma das saídas ativas. A aplicação mantém o saldo cacheado e oferece reconciliação a partir do histórico.

## DT013 — Quantidades inteiras e positivas
**Decisão:** cada movimentação usa quantidade inteira maior que zero. Não permitir saída ou operação que resulte em saldo negativo.  
**Justificativa:** simplificar e tornar inequívoco o controle de unidades no MVP. Quantidades fracionárias podem ser avaliadas em versão futura.

## DT014 — Edição e cancelamento de movimentações
**Decisão:** movimentações podem ser editadas e canceladas logicamente. SKU relacionado não pode ser alterado na edição.  
**Regra de edição:** calcular saldo resultante como saldo atual menos efeito antigo mais efeito novo; rejeitar se ficar negativo.  
**Regra de cancelamento:** reverter efeito; rejeitar cancelamento de entrada quando a reversão gerar saldo negativo. Para relacionar a outro produto, cancelar e criar nova movimentação.

## DT015 — Valores monetários
**Decisão:** usar `Decimal` para cálculos e armazenar preços no JSON como strings decimais com duas casas, por exemplo `"120.00"`.  
**Justificativa:** evitar imprecisão de ponto flutuante em valores monetários. Preços são opcionais e não negativos.

## DT016 — Datas
**Decisão:** armazenar datas como ISO 8601 com timezone UTC. Converter para horário local somente na apresentação.  
**Justificativa:** consistência temporal e ordenação previsível.

## DT017 — Diretório de dados
**Decisão:** em desenvolvimento, usar diretório `data/` do projeto. Na versão empacotada, usar diretório de dados do usuário no Windows, preferencialmente `%LOCALAPPDATA%/ControleEstoque/data`, sem gravar dentro do executável.  
**Justificativa:** diretórios de instalação podem não permitir escrita; separar dados do binário facilita atualizações.

## DT018 — Escrita segura e recuperação
**Decisão:** gravar JSON em arquivo temporário no mesmo diretório e substituir o destino com operação atômica quando suportada (`os.replace`). Tratar falhas e manter backup/recuperação conforme viabilidade. Após operações multi-arquivo interrompidas, reconciliar saldo e reconstruir índices a partir dos registros canônicos.  
**Justificativa:** JSON não oferece transações. O MVP deve reduzir risco e detectar inconsistências sem tentar implementar um banco completo.

## DT019 — Escopo local de instância única
**Decisão:** MVP destinado a uma instância local da aplicação, sem suporte a escrita multiusuário simultânea.  
**Justificativa:** arquivos JSON não oferecem controle transacional/concorrência robusto para uso compartilhado em rede. Documentar a limitação.

## DT020 — Empacotamento
**Decisão:** utilizar PyInstaller para gerar executável Windows com janela gráfica, sem console (`--windowed`). Preferir inicialmente `--onefile` para distribuição simples; se testes identificarem problemas ou lentidão excessiva, avaliar `--onedir`.  
**Justificativa:** incluir interpretador e dependências para execução em máquina sem Python. Build Windows deve ser gerado/testado em Windows.

## DT021 — Testes
**Decisão:** priorizar testes unitários das regras de negócio e testes de persistência com diretórios temporários.  
**Cobertura mínima:** unicidade de SKU, geração automática, entrada, saída, bloqueio de saldo negativo, edição/cancelamento de movimento, exclusão lógica, reconstrução de índice e persistência após reinício.

## DT022 — Transparência no uso de IA
**Decisão:** documentar que a IA foi utilizada para gerar código e apoiar análise, enquanto o usuário definiu escopo, requisitos e decisões e deverá revisar/validar os resultados.  
**Justificativa:** o desafio avalia também a utilização consciente de IA; não atribuir ao usuário autoria manual de código gerado pela ferramenta.

## DT023 — Ferramenta de testes
**Decisão:** utilizar `pytest` como única ferramenta de testes automatizados.
**Justificativa:** decisão expressa do usuário; sua sintaxe concisa atende bem aos testes unitários e de persistência do MVP.

## DT025 — SKU exclusivamente automático
**Decisão:** o SKU será sempre gerado pelo sistema; o cadastro não aceita SKU manual.
**Justificativa:** alteração aprovada pelo usuário para simplificar o cadastro e preservar a identificação única.

## DT026 — Resumo do dashboard
**Decisão:** exibir as 5 últimas movimentações ativas sob “Últimas movimentações” e os produtos ativos com saldo menor que 5 sob “Produtos com saldo baixo”.
**Justificativa:** alteração aprovada pelo usuário para um dashboard mais conciso e legível.

## DT024 — Arquivo JSON inválido
**Decisão:** quando um arquivo JSON estiver inválido ou não puder ser lido, interromper a operação afetada e informar claramente o caminho do arquivo. Não tentar corrigir ou sobrescrever automaticamente o registro.
**Justificativa:** preservar a evidência para correção segura e evitar perda de dados causada por uma recuperação especulativa.

## DT027 — Arquivos de distribuição isolados
**Decisão:** manter os arquivos de configuração e automação do PyInstaller, o ambiente virtual, os artefatos intermediários e o executável em `dir_exe/`, pasta local ignorada integralmente pelo Git.
**Justificativa:** separar a preparação local da distribuição do código-fonte versionado; o executável será publicado como anexo de uma GitHub Release.

## DT028 — Diretório de dados do executável
**Decisão:** em modo empacotado, usar `LOCALAPPDATA` para localizar `%LOCALAPPDATA%/ControleEstoque/data`, com fallback para `AppData/Local` dentro da pasta do usuário quando a variável não existir. Em desenvolvimento, continuar usando `data/` na raiz do projeto.
**Justificativa:** manter dados do usuário fora da pasta de instalação e do diretório temporário do PyInstaller, como definido na DT017.

## DT029 — Build Windows local e publicação
**Decisão:** gerar localmente em Windows um executável `--onefile --windowed`; não incluir os scripts nem o executável no repositório. Distribuir o binário como anexo de uma GitHub Release.
**Justificativa:** manter o repositório de código separado do artefato de download e não versionar binários de build.
