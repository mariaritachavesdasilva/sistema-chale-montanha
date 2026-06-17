# 🗺️ 06-WIREFRAME_IDEAS.md: Arquitetura Visual e Esboços

## 📑 1. Objetivo da Arquitetura

Este documento serve como o "esqueleto" e guia visual para a implementação pela Agente Cleide (Frontend). Ela garante a aplicação da *Regra 80/20* (focar no que gera reservas) e do princípio *Data-First*, onde a interface gráfica respeita rigorosamente os campos estabelecidos no contrato do SCHEMA.md.

---

## 👥 2. Diagrama de Caso de Uso (DCU)

mermaid
useCaseDiagram
    actor "Hóspede (Mobile)" as H
    actor "Anfitrião (Admin)" as A
    
    package "Motor de Reservas Autônomo" {
        usecase "Consultar Datas Livres" as UC1
        usecase "Preencher Dados de Contato" as UC2
        usecase "Finalizar Reserva (WhatsApp/Pix)" as UC3
        usecase "Visualizar Painel de Gestão" as UC4
        usecase "Cancelar/Aprovar Reserva" as UC5
    }
    
    H --> UC1
    H --> UC2
    UC2 ..> UC3 : <<include>>
    A --> UC4
    A --> UC5
```

---

 ## 📱 3. Wireframe: Tela do João (Mobile-First)

Foco: Despertar desejo e concluir a reserva em < 3 minutos.

*Estrutura Visual da Página Única (Single Page):*

1. *Hero Section (Topo):* * Foto principal do chalé em alta resolução (formato WebP para carregar instantaneamente).
* Título convidativo e um botão âncora "Ver Disponibilidade" que rola a página para o calendário.


2. *Card Central (Glassmorphism Orgânico):*
* Painel translúcido (blur) flutuando sobre uma imagem de fundo natural (ex: montanhas, floresta).
* *Calendário Dinâmico:* Destaca os dias livres e risca/bloqueia visualmente os dias já ocupados.
* *Formulário Enxuto:*
* guest_name: Input com ícone de perfil.
* guest_whatsapp: Input com teclado numérico formatado.
* guest_email: Input de contato secundário.




3. *Resumo de Valores:* Cálculo automático exibido na tela assim que os dias de check-in e check-out são selecionados.
4. *Botão CTA:* "Garantir Minha Reserva" (Cor vibrante, contrastante e com área de clique grande para o polegar).


---

## 🖥️ 4. Wireframe: Painel da AnaMaria (Desktop Admin)

Foco: Visão rápida da agenda e gestão sem estresse.

*Estrutura Visual:*

1. *Header Administrativo:* Logo do Chalé, botão "Sair" e indicador de "Token Ativo".
2. *Dashboard Resumo:*
* Próximos Check-ins da semana.
* Total de reservas pendentes.


3. *Tabela de Reservas:*
* Colunas: ID | Hóspede | WhatsApp | Entrada | Saída | Status.
* Botões de ação em cada linha: Confirmar Pagamento (Verde) / Cancelar (Vermelho).

---

## 🔄 5. Diagrama de Sequência (Fluxo de Dados)

Detalhamento da interação desde o clique do hóspede até a proteção contra overbooking no motor da AnaMaria.

mermaid
sequenceDiagram
    participant H as Celular do Hóspede (Cleide)
    participant S as Motor Flask (AnaMaria)
    participant DB as SQLite (chalet.db)
    
    H->>S: GET /api/disponibilidade
    S-->>H: Retorna JSON com dias ocupados
    Note over H: Hóspede seleciona as datas livres e preenche dados
    H->>S: POST /api/reservar (JSON Payload)
    Note over S: Valida datas cruzando com SCHEMA
    S->>DB: Verifica conflito (Query Anti-Overbooking)
    alt Datas Livres
        DB->>DB: INSERT INTO reservas
        S-->>H: Status 201 (Sucesso + Resumo para o Pix)
    else Conflito de Datas
        S-->>H: Status 409 (Erro de Overbooking)
    end


---

## 🎨 6. Mock Data e Estética (The Vibe)

Para validar a interface antes da conexão real com o backend, o Agente Cleide deve usar:

* *Paleta de Cores:* Tons terrosos, verdes profundos (floresta) ou neutros elegantes (bege/branco), com elementos glass garantindo sofisticação.
* *Comportamento:* * Ao selecionar os dias, uma animação suave deve revelar o valor da estadia.
* Ao clicar em reservar, exibir um "Spinner" de carregamento e, após o sucesso, substituir o formulário por um "Ticket de Reserva" elegante com o botão "Enviar Comprovante no WhatsApp".


* *Resiliência Visual:* Se o hóspede perder a conexão de internet bem na hora de preencher, o formulário não deve apagar os dados dele.


---

### 🛂 Instrução para a IA
>
> *"Cleide, use este wireframe como base inegociável para o `index.html`. Não adicione 'enfeites' que aumentem a latência ou o consumo de dados. AnaMaria, certifique-se de que o motor backend suporte exatamente o fluxo descrito no Diagrama de Sequência."*