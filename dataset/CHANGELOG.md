Este conjunto de dados apresenta a demanda de passageiros do Metrô de Belo Horizonte, sob gestão da Secretaria de Estado de Infraestrutura, Mobilidade e Parcerias (SEINFRA/MG).

Os dados são consolidados a partir das transações registradas no sistema de bilhetagem do Metrô BH. Cada mês de referência traz todas as transações de uma semana completa, a 3ª semana do mês, de domingo a sábado. Para cada transação são informados a data e a hora, a estação e o bloqueio em que ocorreu, o grupo de bilhetagem, a forma de pagamento, o tipo de bilhetagem e, quando registrado, o valor pago.

Arquivos: um recurso por mês de referência, com o nome metro_AAAA_MM (CSV, separador ponto e vírgula, UTF-8, decimal com vírgula). Granularidade: uma linha por transação. Atualização mensal.

Dicionário de dados

id_transacao – integer: identificador da transação no sistema de bilhetagem. data_hora – datetime (AAAA-MM-DD HH:MM:SS.mmm): data e hora da transação. id_estacao – integer: código da estação em que ocorreu a transação. id_bloqueio – integer: código do bloqueio (catraca) em que ocorreu a transação. grupo_bilhetagem – string: grupo da bilhetagem. Valores: Exclusivos, Integrados, Gratuidades. forma_pagamento – string: meio usado na transação. Valores: VALIDADOR EXTERNO, QRCODE, CARTAO SERVICO, CARTAO BANCARIO. tipo_bilhetagem – string: tipo da bilhetagem. Ex.: Transfacil, Otimo, Bilheteria, Passe Livre, Credito, Debito, App Bipay, Operacional. valor – number: valor pago na transação, em reais. Preenchido apenas quando registrado pelo sistema (pagamentos por QR Code e cartão bancário); vazio nas demais formas de pagamento. id_validador – string: identificador do validador, quando informado pelo sistema de bilhetagem. usuario – string: código pseudonimizado do usuário, preenchido apenas quando a forma de pagamento identifica o usuário. Ex.: f942de2fb6952a48.

Observações

Cada mês traz apenas a 3ª semana completa do mês (de domingo a sábado), e não o mês inteiro. O período exato e o total de transações de cada arquivo estão na descrição do recurso. A coluna usuario é pseudonimizada (HMAC-SHA256), em atendimento à Lei Geral de Proteção de Dados (LGPD). O mesmo usuário recebe o mesmo código em todos os meses, o que permite acompanhar padrões de uso sem identificar a pessoa. As alterações e reprocessamentos de cada publicação estão registrados no histórico de alterações abaixo.

# CHANGELOG - Controle de alterações

Documentação das principais alterações deste repositório.
Baseado na filosofia [Mantenha um Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

### [1.10.2] - 2026-11-26

- Atualizado o recurso `metro_2026_07` (Demanda bilhetagem Metro BH 07/2026): 3ª semana de 19/07/2026 a 25/07/2026, 437.726 transações.

### [1.10.1] - 2026-11-26

- Atualizado o recurso `metro_2026_07` (Demanda bilhetagem Metro BH 07/2026): 3ª semana de 19/07/2026 a 25/07/2026, 437.726 transações.

### [1.10.0] - 2026-11-24

- Incluído o recurso `metro_2026_09` (Demanda bilhetagem Metro BH 09/2026): 3ª semana de 20/09/2026 a 26/09/2026, 481.393 transações.

### [1.9.0] - 2026-11-24

- Incluído o recurso `metro_2026_08` (Demanda bilhetagem Metro BH 08/2026): 3ª semana de 16/08/2026 a 22/08/2026, 492.008 transações.

### [1.8.0] - 2026-11-24

- Incluído o recurso `metro_2026_07` (Demanda bilhetagem Metro BH 07/2026): 3ª semana de 19/07/2026 a 25/07/2026, 437.726 transações.

### [1.7.0] - 2026-11-24

- Incluído o recurso `metro_2026_06` (Demanda bilhetagem Metro BH 06/2026): 3ª semana de 21/06/2026 a 27/06/2026, 470.482 transações.

### [1.6.0] - 2026-11-24

- Incluído o recurso `metro_2026_05` (Demanda bilhetagem Metro BH 05/2026): 3ª semana de 17/05/2026 a 23/05/2026, 498.512 transações.

### [1.5.0] - 2026-11-24

- Incluído o recurso `metro_2026_04` (Demanda bilhetagem Metro BH 04/2026): 3ª semana de 19/04/2026 a 25/04/2026, 400.542 transações.

### [1.4.0] - 2026-11-24

- Incluído o recurso `metro_2026_03` (Demanda bilhetagem Metro BH 03/2026): 3ª semana de 15/03/2026 a 21/03/2026, 477.923 transações.

### [1.3.2] - 2026-11-24

- Atualizado o recurso `metro_2026_02` (Demanda bilhetagem Metro BH 02/2026): 3ª semana de 15/02/2026 a 21/02/2026, 454.215 transações.

### [1.3.1] - 2026-11-12

- Atualizado o recurso `metro_2026_02` (Demanda bilhetagem Metro BH 02/2026): 3ª semana de 15/02/2026 a 21/02/2026, 454.215 transações.

### [1.3.0] - 2026-11-12

- Incluído o recurso `metro_2026_02` (Demanda bilhetagem Metro BH 02/2026): 3ª semana de 15/02/2026 a 21/02/2026, 454.215 transações.

### [1.2.0] - 2026-11-12

- Incluído o recurso `metro_2026_01` (Demanda bilhetagem Metro BH 01/2026): 3ª semana de 18/01/2026 a 24/01/2026, 388.864 transações.

### [1.1.0] - 2026-11-12

- Incluído o recurso `metro_2026_10` (Demanda bilhetagem Metro BH 10/2026): 3ª semana de 18/10/2026 a 24/10/2026, 509.311 transações.

### [1.0.0] - 2026-11-12

- Versão inicial
