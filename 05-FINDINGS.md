# 🧠 05-FINDINGS.md: Memória Técnica e Log de Autocura

## 🎯 1. Propósito e Uso

Este arquivo é o **Cérebro de Recuperação** do projeto. Sempre que ocorrer um erro de execução no servidor Flask, um bug visual no calendário ou uma falha na lógica de proteção contra overbooking, o erro deve ser colado aqui antes de solicitar a correção à IA.

**Protocolo de Autocura:**

1. Copie o erro/traceback do terminal (Backend) ou console do navegador (Frontend).
2. Cole na seção **Log de Incidentes** abaixo.
3. Invoque a IA com o comando: "Analise os erros no FINDINGS.md, identifique a causa raiz e aplique uma correção cirúrgica no código".

---

## 📋 2. Log de Incidentes e Erros (The Log)

**Utilize esta tabela para registrar falhas técnicas e comportamentais da IA durante as sessões.**

| Data | Componente | Descrição do Erro / Traceback | Causa Raiz | Correção Cirúrgica Aplicada |
| --- | --- | --- | --- | --- |
| 2026-06-09 | AnaMaria (Backend) | `UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e5' in position 0: character maps to <undefined>` ao tentar imprimir emojis no terminal Windows. | O stdout do console no Windows usa por padrão a codificação `cp1252`, que não suporta caracteres emoji Unicode de 4 bytes. | Remover os emojis dos comandos `print` ou forçar a codificação UTF-8 de stdout. Decidido por simplificar as strings de log de texto removendo caracteres especiais. |
| [Data] | [AnaMaria/Cleide] | [Cole o erro aqui] | [Ex: Alucinação de coluna no banco] | [Resumo da mudança] |

---

## 🔬 3. Análise de Causa Raiz (Root Cause) e Padrões

Espaço para documentar por que erros recorrentes estão acontecendo na construção do site.

* **Padrão Detectado:** (Ex: A IA (Ana) insiste em usar caminhos relativos para o arquivo chalet.db em vez de os.path.abspath).
* **Ação Preventiva:** (Ex: Reforçar a regra de "Caminhos Absolutos" no 04-BACKEND_GUIDE.md para garantir que a hospedagem VPS não falhe ao reiniciar).

---

## 💡 4. Decisões Técnicas e Trade-offs (Findings)

Conforme as Karpathy Guidelines ("Think Before Coding"), registre aqui as premissas assumidas antes de grandes mudanças na arquitetura do chalé.

**Decisão:** Uso de SQLite puro sem ORM (Object-Relational Mapping).
**Justificativa:** Garantir que a arquitetura seja autocontida (Self-Contained) e leve, permitindo rodar em servidores baratos e seguindo a regra de simplicidade 80/20.


**Decisão:** Design Glassmorphism Orgânico com abordagem Mobile-First.
**Justificativa:** Foco absoluto na experiência do visitante, que em 90% dos casos acessará o site pelo celular. A interface translúcida valoriza as fotos do chalé ao fundo.


**Decisão:** Fechamento de reserva via WhatsApp/Pix no MVP.
**Justificativa:** Adiar integrações complexas (e taxadas) de gateways de cartão de crédito para focar na validação rápida do sistema de disponibilidade.

---

## 🚧 5. Devedor Técnico e Lições Aprendidas

*O que ficou para o próximo giro do PDCA ou o que aprendemos que não deve ser repetido.*

1. **Lição:** Nunca usar fotos do chalé em .png ou .jpg pesados na tela inicial. Isso aumenta a taxa de rejeição. Usar exclusivamente .webp com lazy loading.
2. **Lição:** A validação de datas conflitantes (overbooking) não pode confiar apenas no calendário do Frontend (Cleide). A AnaMaria (Backend) deve fazer a dupla verificação no banco antes de qualquer INSERT.
3. **Dívida:** O envio automatizado de e-mails ("Sua reserva foi confirmada") ficará para a Fase 2 (Evolução). O MVP dependerá do contato humano ou via link dinâmico de WhatsApp
4. **Lição:** Em sistemas Windows sem Python global instalado, os atalhos da Microsoft Store interceptam o executável `python` e causam falhas. A instalação e o uso do `uv` (`uv run ...`) é a forma ideal para baixar e gerenciar o interpretador e as dependências isoladamente.
---

### 🛂 Instrução para a IA
>
> *"Antes de cada correção de código, consulte as seções 2 e 4 deste arquivo para garantir que a nova solução não repita erros do passado e mantenha as decisões arquiteturais (como a proteção contra overbooking e o formato SQLite) já validadas".*
