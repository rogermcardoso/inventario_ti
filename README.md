# Inventário de TI – Flask + SQLite

Sistema web para controle de inventário de equipamentos de TI, usuários e movimentações, baseado em **patrimônio** como chave principal do equipamento.

Este projeto foi construído para:

- controlar equipamentos (notebook, desktop, etc)
- controlar usuários
- registrar histórico completo de movimentações
- permitir drill-down por patrimônio
- preparar futura integração com OCS Inventory
- facilitar futura migração para PostgreSQL

---

## Funcionalidades

### Equipamentos
- cadastro por número de patrimônio (chave primária lógica)
- status da máquina (disponível, alocado, manutenção, descartado, roubado, etc)
- informações técnicas e administrativas
- histórico de manutenção (campos no cadastro)

### Usuários
- nome
- cargo
- centro de custo
- departamento
- termo assinado (S/N)

### Movimentações
- baseadas no patrimônio do equipamento
- registra:
  - usuário anterior
  - novo usuário
  - data
  - observação
- mantém histórico permanente
- troca automaticamente o usuário atual do equipamento

### Histórico por patrimônio
- tela de histórico (drill-down) mostrando todas as movimentações do equipamento

---

## Estrutura do projeto
inventario_ti/
│
├── app.py
├── init_db.py
├── schema.sql
├── sync_ocs.py
│
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── equipamentos.html
│ ├── equipamento_form.html
│ ├── equipamento_detalhe.html
│ ├── usuarios.html
│ ├── usuario_form.html
│ ├── movimentacoes.html
│ ├── movimentacao_form.html
│ └── historico_patrimonio.html
│
├── static/
│ ├── custom.css
│ └── favicon.ico
│
└── inventario_ti.db (não versionar)

---

## Requisitos

- Python 3.9+
- Flask

Instalação do Flask:
pip install flask


---

## Criação do banco de dados

O banco é criado a partir do schema.

Você pode usar o script de inicialização:

python init_db.py


Este script:

- cria o arquivo `inventario_ti.db`
- executa todo o conteúdo do `schema.sql`

---

## Executando o sistema

python app.py


Depois acesse:
http://127.0.0.1:5000


---

## Modelagem principal

### Equipamentos

- patrimonio
- tipo
- marca
- modelo
- numero_serie
- sistema_operacional
- memoria
- ano_compra
- status_maquina
- status_usuario
- usuario_atual_id
- observacoes
- ultima_manutencao_preventiva
- manutencao_preventiva_programada

### Usuários

- id
- nome_usuario
- cargo
- centro_custo_id
- departamento_id
- termo_assinado

### Centros de custo

- id
- codigo
- nome

### Departamentos

- id
- nome

### Movimentações

- id
- patrimonio
- usuario_anterior_id
- usuario_novo_id
- data_movimentacao
- obs

---

## Fluxo de movimentação

1. seleciona o patrimônio
2. o sistema carrega automaticamente o usuário atual
3. seleciona o novo usuário
4. salva a movimentação
5. atualiza o usuário atual do equipamento
6. mantém todo o histórico

---

## Integração com OCS Inventory

O arquivo:


sync_ocs.py


é responsável por buscar dados no banco do OCS Inventory e atualizar:

- equipamentos
- informações técnicas

A ideia é usar esse script de forma independente (job ou agendamento).

---

## Observação importante

O projeto foi estruturado para facilitar:

- sincronização automática de inventário
- futura migração de banco

---

## Migração futura para PostgreSQL

A estrutura foi pensada para que a troca de SQLite para PostgreSQL seja simples.

Em termos práticos, será necessário:

- trocar o driver de conexão
- ajustar a criação de conexão
- revisar pequenas diferenças de tipos

A modelagem não precisará ser refeita.

---

## Segurança

O arquivo de banco:


inventario_ti.db


não deve ser versionado.

Use no `.gitignore`:


inventario_ti.db


---

## Observação final

Este sistema foi projetado para uso em ambientes de TI corporativos, com foco em:

- rastreabilidade de ativos
- governança
- histórico de uso
- integração com ferramentas de inventário automático