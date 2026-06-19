# 🏡 Projeto VEM — Sistema Inteligente de Gestão de Reservas para Chalés

## Visão Geral

O Projeto VEM foi desenvolvido como trabalho acadêmico com o objetivo de facilitar a gestão de reservas de um chalé, centralizando informações e reduzindo o trabalho manual do proprietário.

A proposta surgiu da necessidade de organizar reservas realizadas por diferentes plataformas, como Airbnb e Booking, permitindo um controle mais eficiente da ocupação, disponibilidade e informações dos hóspedes.

## Problema

Atualmente, proprietários que anunciam em múltiplas plataformas precisam acompanhar reservas em diferentes sistemas, aumentando o risco de erros, conflitos de datas e retrabalho.

## Solução

O sistema atua como uma ferramenta de apoio à gestão de reservas, oferecendo:

* Consulta de disponibilidade;
* Cadastro e gerenciamento de reservas;
* Controle de hóspedes;
* Histórico de ocupação;
* Persistência local dos dados;
* Interface simples e intuitiva;
* Arquitetura preparada para integração com plataformas de hospedagem.

## Objetivo Acadêmico

Aplicar conceitos de Engenharia de Software, Engenharia de Requisitos, Arquitetura de Sistemas, Banco de Dados e Inteligência Artificial na construção de uma solução prática para um problema real.

## Tecnologias Utilizadas

* Frontend
* Backend
* SQLite
* Arquitetura Orientada a Agentes
* RAG (Memória e documentação)
* MCP (Integração segura de ferramentas)
* Antigravity (Orquestração de agentes)

## Resultados Esperados

* Redução de erros no gerenciamento de reservas;
* Maior organização das informações dos hóspedes;
* Melhor controle da disponibilidade do chalé;
* Base tecnológica preparada para futuras integrações com Airbnb e Booking.

---

# 🏁 Arquitetura Orientada a Agentes

## Filosofia

Do problema real ao deploy em produção: formando engenheiros de software capazes de transformar requisitos em soluções resilientes através da colaboração entre humanos e agentes de IA.

O Projeto VEM integra princípios de Engenharia de Requisitos, Spec-Driven Development (SDD), AI-First Engineering e simplicidade orientada a valor. O objetivo é garantir que cada funcionalidade exista por uma necessidade real do usuário, evitando complexidade desnecessária e reduzindo alucinações dos agentes.

## 🏗️ Arquitetura Padrão Ouro

```text
Usuário
   ↓
Frontend
   ↓
Antigravity (Orquestração)
   ↓
Agentes Especializados
   ├── RAG (Memória)
   ├── MCP (Ferramentas)
   └── Plugins
   ↓
Banco de Dados Local (SQLite)
```

### Camadas

#### Frontend

Responsável pela experiência do usuário, acessibilidade e comunicação com os agentes.

#### Antigravity

Camada de orquestração responsável pelo gerenciamento de contexto, fluxo de execução, coordenação entre agentes, integração com MCP e consulta à memória RAG.

#### Agentes

Executam tarefas especializadas seguindo as regras definidas na documentação do projeto.

#### RAG (Retrieval-Augmented Generation)

Base de conhecimento utilizada para consulta de requisitos, regras de negócio, padrões técnicos e histórico do projeto.

#### MCP (Model Context Protocol)

Camada segura de ferramentas utilizada pelos agentes para acesso controlado a banco de dados, arquivos e recursos locais.

#### SQLite

Persistência local seguindo o princípio Offline-First.

## 🧠 Fontes da Verdade

### Regras de Negócio e Governança

Os arquivos localizados em `/rag/memoria/`, `/docs` e os arquivos `.md` da raiz representam a fonte oficial para requisitos, decisões arquiteturais, processos e governança.

### Estrutura de Dados

O arquivo `SCHEMA.md` é a fonte única da verdade para contratos de dados, APIs, formulários e persistência.

> JSON is Law.

Toda alteração estrutural deve partir do SCHEMA.md.

## 🛂 Agentes Especializados

### José — Frontend

Responsável por UI, UX, acessibilidade e experiência do usuário.

### Ana — Backend

Responsável por lógica de negócios, persistência e integração.

### Maria — Auditoria

Responsável por conformidade, qualidade de requisitos e governança.

### Tiago — QA

Responsável por testes unitários, integração e validação E2E.

### Piloto — Deploy

Responsável por empacotamento, publicação e entrega.

## ⚖️ Regras Inegociáveis

* Pense antes de codar.
* Regra 80/20.
* Mudanças cirúrgicas.
* Offline-First.
* Documentação antes da implementação.
* JSON is Law.

## 🔄 Fluxo Operacional

1. Contexto (VCC)
2. Planejamento
3. Build
4. Check
5. Learn
6. Ship

## 🎯 Objetivo Final

Transformar problemas reais em software utilizável, resiliente e rastreável através de uma metodologia estruturada que combine Engenharia de Requisitos, IA Generativa, Arquitetura Orientada a Agentes e desenvolvimento guiado por especificações.
