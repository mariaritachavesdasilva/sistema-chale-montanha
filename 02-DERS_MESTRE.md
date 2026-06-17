# 📝 02-DERS_MESTRE.md: Especificação Mestre de Requisitos

## 📑 1. Identificação e Controle de Versão

- **Projeto:** Sistema Autônomo de reservas de Chalé.
- **Versão:** 1.0 (Baseada no VEM).
- **Responsáveis:** Gestão de Chalé e Desenvolvedor.
- **Histórico:** Criação do escopo técnico baseado no North Star.

---

## 🎯 2. Visão Geral e Escopo

- **Objetivo Central:** Garantir que os hóspedes consigam consultar disponibilidade e fechar reservas de forma autônoma e rápida.
- **Público-Alvo:** O Hóspede (que deseja garantir sua data facilmente pelo celular) e O Anfitrião (que precisa de controle de agenda sem esforço manual).
- **Fora de Escopo:** Aplicativos nativos para lojas, logins complexos, programas de fidelidade e integrações pesadas de gateway de pagamento logo na V1.

---

## 👥 3. Requisitos de Usuário (RU)

*Descrições abstratas das necessidades, escritas em linguagem natural para stakeholders.*

- **RU01:** O hóspede deseja ver fotos, verificar os dias livres no calendário e registrar sua reserva pelo celular em poucos minutos.
- **RU02:** O anfitrião deseja ter um painel simples para visualizar quais dias estão ocupados e os dados de contato dos hóspedes confirmados.

---

## ⚙️ 4. Requisitos de Sistema (RS)

*Detalhamento técnico das funções para orientar a implementação pela IA.*

- **RS01:** O sistema deve cruzar as datas selecionadas pelo usuário com o banco de dados em tempo real para impedir overbooking (reservas duplas).
- **RS02:** O motor de persistência deve utilizar um banco de dados leve (como SQLite) para garantir respostas rápidas e facilidade de backup/migração de servidor.

---

## ✅ 5. Requisitos Funcionais (RF) e Priorização

*Funcionalidades específicas mapeadas por prioridade.*

| ID | Descrição do Requisito | Tipo | Prioridade | Critério de Aceite (Sucesso) |
| :--- | :--- | :--- | :--- | :--- |
| **RF01** | Calendário dinâmico de disponibilidade. | RS | **Essencial** | Bloqueia visualmente datas já reservadas ou em manutenção |
| **RF02** | Painel administrativo protegido. | RS | **Importante** | Permite ao anfitrião aprovar, cancelar ou adicionar reservas manuais. |
| **RF03** | Captura de dados Check-in, Check-out, Nome, Telefone, Email. | RS | **Essencial** |  Formulário limpo que salva a intenção de reserva no banco.|
| **RF04** | Redirecionamento para fechamento (Pix/WhatsApp). | RS | *Essencial* | Após preencher o formulário, gera resumo e link de pagamento. |

> **Legenda de Prioridade:**
>
>  **Essencial:** O site não gera faturamento sem isso (Regra 80/20).
>  **Importante:** Agiliza a gestão, mas pode ser contornado manualmente no início.
>  **Desejável:** Funcionalidades de luxo (ex: e-mails automatizados).

---

## 📏 6. Regras de Negócio (RN)

*Restrições que controlam a operação e a integridade do sistema.*

| ID | Descrição da Regra | Requisito Relacionado |
| :--- | :--- | :--- |
| **RN01**| A data de check-out deve ser obrigatoriamente posterior à data de check-in. | RF02 |
| **RN02**| Uma nova reserva não pode sobrepor total ou parcialmente os dias de uma reserva já com status "Confirmada". | RF01, RS01 |
| **RN03**| Reservas iniciadas que não tiverem o pagamento confirmado em até X horas voltam a ficar disponíveis. | RF01, RF04 |

---

## 🛡️ 7. Requisitos Não Funcionais (RNF)

*Atributos de qualidade seguindo o modelo **FURPS**.*

| ID | Nome / Atributo | Categoria | Prioridade | Descrição Técnica |
| :--- | :--- | :--- | :--- | :--- |
| *RNF01* | Mobile-First | Usabilidade | **Essencial** | A interface de reserva deve ser impecável em telas de celular. |
| *RNF02* | Performance Visual | Performance | **Essencial** | Fotos do chalé devem ser carregadas rapidamente (arquivos otimizados/WebP). |
| *RNF03* | Confiabilidade de Sessão | Segurança | **Importante** | O painel do administrador deve ser inacessível sem token válido. |

---

## ⚖️ 8. Diretrizes Karpathy de Implementação (VEM)

*Instruções comportamentais inegociáveis para a IA José e Ana.*

1. **Pense antes de codar:** Desenhe o fluxo da reserva antes de escrever a primeira tag HTML.
2. **Simplicidade Radical:** Nada de frameworks JavaScript pesados no front-end se um bom HTML5, CSS3 e JS Vanilla derem conta do recado com elegância.
3. **Foco na Conversão:** Menos cliques possíveis entre "ver a foto" e "apertar em reservar".

---

## 🔗 9. Matriz de Rastreabilidade Simples

*Mapeamento para garantir que nenhum objetivo do North Star foi esquecido.*

- **RU01** → RF01, RF02, RF03, RNF01.
- **RU02** → RF04, RS01, RNF03, RN03.

---

**💡 Instrução para a IA:** Se durante o desenvolvimento for solicitada uma função que não esteja listada neste documento, você deve "empurrar de volta" (*push back*) citando a soberania do DERS e da Regra 80/20.
