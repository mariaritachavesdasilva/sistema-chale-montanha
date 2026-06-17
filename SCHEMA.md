# 📊 05-SCHEMA.md: Constituição dos Dados e Contratos de API (Site do Chalé)

## 📑 1. Identificação do Modelo

*Projeto:* Sistema Autônomo de Reservas de Chalé (MVP)

*Arquiteta de Dados:* AnaMaria (Backend)

*Revisora:* Maria (Conformidade/LGPD)

*Versão:* 1.0

---

## 🏛️ 2. Entidades e Atributos (The Law)

Esta tabela define os campos que serão persistidos no banco de dados SQLite local. Nenhuma implementação pode adicionar campos "enfeite" fora desta lista.

### 🏡 Tabela: reservas

| Campo | Tipo (SQLite) | Restrição | Descrição |
| --- | --- | --- | --- |
| id | Integer | Primary Key | Identificador único autoincremento da reserva. |
| guest_name | String | Not Null | Nome completo do hóspede preenchido no formulário. |
| guest_whatsapp | String | Not Null | Número com DDD (apenas dígitos, formatado pela Ana). |
| guest_email | String | Not Null | E-mail para contato secundário. |
| checkin_date | String | Not Null | Data de entrada no formato ISO YYYY-MM-DD. |
| checkout_date | String | Not Null | Data de saída no formato ISO YYYY-MM-DD. |
| status | String | Default: 'pendente' | Controle do anfitrião (pendente, confirmada, cancelada). |
| total_price | Real | Not Null | Valor total da estadia calculado no envio. |
| created_at | DateTime | Default: NOW | Data e hora automática da criação da reserva. |

---

## 📜 3. Contrato de API (JSON is Law)

Este é o formato exato que as requisições e respostas devem seguir entre o calendário do celular e o motor do servidor.

### 📥 Entrada de Reserva (POST /api/reservar)

json
{
  "guest_name": "Carlos Silva",
  "guest_whatsapp": "11999999999",
  "guest_email": "carlos@email.com",
  "checkin_date": "2026-08-10",
  "checkout_date": "2026-08-15",
  "total_price": 1250.00
}



### 📤 Saída de Disponibilidade (GET /api/disponibilidade)

Usado pelo calendário para bloquear as datas que já foram vendidas.

json
{
  "dates_booked": [
    "2026-08-10",
    "2026-08-11",
    "2026-08-12",
    "2026-08-13",
    "2026-08-14"
  ]
}



---

## 🛡️ 4. Regras de Integridade e Validação

1. *Anti-Overbooking Absoluto:* O banco de dados rejeitará qualquer tentativa de INSERT se as datas de checkin_date e checkout_date colidirem com uma reserva cujo status seja diferente de cancelada.
2. *Minimização (LGPD):* Não é permitida a coleta de CPF, RG ou endereço completo do hóspede nesta fase do MVP, respeitando a privacidade por design e mantendo a conversão alta.
3. *Segurança Administrativa:* A rota do painel do anfitrião (GET /api/admin/reservas) exige obrigatoriamente o Header X-Admin-Token configurado no backend.

---

## 🛂 5. Protocolo de Governança para Agentes

* *AnaMaria (Backend):* Você está proibida de criar rotas ou tabelas que não estejam previstas neste esquema. O banco de dados deve utilizar transações seguras.
* *Cleide (Frontend):* Seus inputs no arquivo index.html e os nomes de chaves no fetch() devem ser idênticos aos nomes (snake_case) desta constituição.
* *Maria (Auditora):* Reprove qualquer código que introduza campos não documentados (ex: pedir data de nascimento) ou que viole a regra de minimização de dados do chalé.

### 💡 Por que este arquivo é vital?

O `SCHEMA.md` elimina o **Vibe Coding** desordenado onde a IA "adivinha" os nomes das colunas. Ele funciona como o alicerce técnico que permite que o frontend e o backend sejam construídos em paralelo com a certeza de que "conversarão" a mesma língua.
