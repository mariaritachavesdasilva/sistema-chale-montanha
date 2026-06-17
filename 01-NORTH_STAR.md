# 01-NORTH_STAR.md: Intenção e Limites do Projeto

## 🎯 1. Intenção Central (The North Star)

Uma única frase que define o sucesso absoluto do projeto.

R: Transformar visitantes curiosos em hóspedes confirmados através de uma experiência de reserva online autônoma, rápida e sem atritos.

## 😫 2. O Problema Real (A Dor)

Qual é a dor do mundo real que estamos resolvendo?
R:Atualmente, reservas feitas exclusivamente por WhatsApp tomam muito tempo de atendimento e podem fazer o cliente esfriar e desistir. Por outro lado, depender apenas de plataformas como Airbnb ou Booking corroem a margem de lucro devido às altas taxas. O dono do chalé precisa de independência e automação, e o hóspede precisa de agilidade para garantir sua data.

## 👥 3. Público-Alvo (As Personas)

O sistema é desenhado para atender às necessidades específicas destes dois perfis:

R: O Hóspede: Quer ver fotos inspiradoras, verificar se a data que ele quer está livre e garantir a reserva em poucos minutos, usando apenas o celular, sem precisar ficar esperando alguém responder no chat.
O Gestor/Anfitrião: Quer receber uma notificação de que a reserva foi feita e paga, com o calendário atualizado automaticamente para evitar overbooking (reservas duplas).

## 🔍 4. Checklist de Descoberta (5 Questões)

Disponibilidade: Um calendário claro e em tempo real mostrando dias livres e ocupados.
Fricção Zero: O hóspede deve conseguir concluir a reserva em menos de 3 minutos.
Independência: O sistema deve funcionar rodando em domínio próprio, fortalecendo a sua marca.
Gestão Visual: Uma área administrativa simples onde você bate o olho e vê quem entra e quem sai na semana.
Interface: Design responsivo, carregamento ultrarrápido das fotos e um botão de "Reservar" sempre visível.

## 🚫 5. Limites e Fora de Escopo

NÃO criaremos aplicativos para lojas (App Store/Play Store) - será um site Web acessível via navegador.
NÃO criaremos, no MVP (Produto Mínimo Viável), programas de fidelidade ou sistemas de pontos complexos.
NÃO faremos integração com dezenas de meios de pagamento diferentes logo de cara (foco no que funciona rápido, como Pix ou cartão via um gateway seguro).

## ⚖️ 6. Mindset de Simplicidade (Karpathy Style)

Este projeto segue a Regra 80/20: 80% do valor operacional será entregue com 20% do código.
Foco do MVP: Uma vitrine de fotos bonita, um calendário de seleção de datas, um formulário curto (Nome, Email, Telefone) e o direcionamento para o pagamento. Isso entrega todo o valor necessário para começar a faturar.

### 🛂 Instrução para a IA

"Antes de iniciar a Fase 2 (Requisitos), leia este arquivo. Qualquer funcionalidade sugerida que fira os limites do Item 5 ou o Mindset do Item 6 deve ser descartada imediatamente".
