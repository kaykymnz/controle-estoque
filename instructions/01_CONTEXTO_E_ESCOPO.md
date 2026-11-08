# Contexto, objetivo e escopo

## Objetivo

Construir um sistema desktop de controle de estoque para um desafio prático de Engenharia de Software. O avaliador quer observar modelagem, desenvolvimento, qualidade, decisões técnicas e uso de IA.

## Experiência esperada

Aplicação visual, simples, limpa e leve. O usuário não deve precisar usar CMD/terminal para operar o sistema.

Tecnologia visual aprovada: **Tkinter + ttk**. Não adotar PySide6, Electron, navegador embutido ou framework pesado sem aprovação expressa.

## Funcionalidades do MVP

1. Cadastrar produto com SKU automático.
2. Editar dados permitidos do produto.
3. Consultar produtos com filtros.
4. Excluir produto logicamente, somente com saldo zero.
5. Registrar entrada e saída.
6. Acessar ações de entrada/saída pela tela de detalhe/consulta do produto.
7. Editar e cancelar movimentações com recálculo consistente do saldo.
8. Consultar histórico de movimentações com filtros.
9. Dashboard com 5 movimentações recentes e produtos ativos com saldo inferior a 5.
10. Persistir dados em arquivos JSON.
11. Executar pelo VS Code e gerar executável Windows.

## Fora do escopo

Não implementar sem aprovação: login, usuários/perfis, múltiplos depósitos, fornecedores, compras, vendas, faturamento, integração com APIs, banco de dados, multiusuário em rede ou estoque mínimo configurável.

## Princípios

- Simplicidade proporcional ao desafio.
- Separação de responsabilidades sem overengineering.
- Regras de negócio testáveis sem interface gráfica.
- Persistência isolada por contratos de repositório.
- Integridade do saldo como regra crítica.
- Documentação honesta e reproduzível.
