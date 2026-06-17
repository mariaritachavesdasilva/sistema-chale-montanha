// Seletores de Elementos do DOM
const calendarGrid = document.getElementById('calendar-grid');
const currentMonthYearHeader = document.getElementById('current-month-year');
const prevMonthBtn = document.getElementById('prev-month');
const nextMonthBtn = document.getElementById('next-month');
const reservationForm = document.getElementById('reservation-form');
const priceSummary = document.getElementById('price-summary');
const summaryNights = document.getElementById('summary-nights');
const summaryTotal = document.getElementById('summary-total');
const btnReserve = document.getElementById('btn-reserve');
const bookingFlow = document.getElementById('booking-flow');
const successFlow = document.getElementById('success-flow');
const toastMessage = document.getElementById('toast-message');

// Estado da Aplicação
let bookedDates = new Set();
let currentYear = new Date().getFullYear();
let currentMonth = new Date().getMonth(); // 0-indexed
let checkinDate = null;  // Objeto Date
let checkoutDate = null; // Objeto Date
const dailyRate = 250.00;

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    fetchBookedDates();
    setupCalendarNavigation();
    setupFormValidation();
});

// Exibir Notificação (Toast)
function showToast(message, duration = 4000) {
    toastMessage.textContent = message;
    toastMessage.style.display = 'block';
    setTimeout(() => {
        toastMessage.style.display = 'none';
    }, duration);
}

// Formatar Data para String ISO YYYY-MM-DD
function formatISODate(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}

// Buscar as datas ocupadas do servidor
async function fetchBookedDates() {
    try {
        const response = await fetch('/api/disponibilidade');
        if (!response.ok) throw new Error('Falha ao buscar disponibilidade.');
        const data = await response.json();
        bookedDates = new Set(data.dates_booked);
        renderCalendar();
    } catch (error) {
        console.error(error);
        showToast('Erro ao carregar o calendário de disponibilidade.');
        renderCalendar();
    }
}

// Configurar navegação de meses do calendário
function setupCalendarNavigation() {
    prevMonthBtn.addEventListener('click', () => {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        renderCalendar();
    });

    nextMonthBtn.addEventListener('click', () => {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        renderCalendar();
    });
}

// Renderizar o calendário na tela
function renderCalendar() {
    calendarGrid.innerHTML = '';
    
    const monthNames = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ];
    
    currentMonthYearHeader.textContent = `${monthNames[currentMonth]} ${currentYear}`;

    // Renderizar cabeçalho dos dias da semana
    const daysOfWeek = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
    daysOfWeek.forEach(day => {
        const headerCell = document.createElement('div');
        headerCell.className = 'day-name';
        headerCell.textContent = day;
        calendarGrid.appendChild(headerCell);
    });

    // Calcular dias do mês
    const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay();
    const totalDays = new Date(currentYear, currentMonth + 1, 0).getDate();
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Células vazias até o primeiro dia da semana
    for (let i = 0; i < firstDayIndex; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'calendar-day disabled';
        calendarGrid.appendChild(emptyCell);
    }

    // Gerar dias do mês
    for (let day = 1; day <= totalDays; day++) {
        const dateObj = new Date(currentYear, currentMonth, day);
        dateObj.setHours(0, 0, 0, 0);
        
        const dateStr = formatISODate(dateObj);
        const dayCell = document.createElement('div');
        dayCell.className = 'calendar-day';
        dayCell.textContent = day;
        dayCell.setAttribute('role', 'gridcell');
        dayCell.setAttribute('aria-label', `Dia ${day} de ${monthNames[currentMonth]} de ${currentYear}`);

        // Verificar se é no passado
        if (dateObj < today) {
            dayCell.classList.add('disabled');
        } 
        // Verificar se está reservado
        else if (bookedDates.has(dateStr)) {
            dayCell.classList.add('booked');
            dayCell.setAttribute('aria-disabled', 'true');
        } 
        // Dia livre para selecionar
        else {
            // Estilizar se estiver selecionado ou no intervalo
            if (checkinDate && dateStr === formatISODate(checkinDate)) {
                dayCell.classList.add('selected');
            } else if (checkoutDate && dateStr === formatISODate(checkoutDate)) {
                dayCell.classList.add('selected');
            } else if (checkinDate && checkoutDate && dateObj > checkinDate && dateObj < checkoutDate) {
                dayCell.classList.add('in-range');
            }

            dayCell.addEventListener('click', () => handleDayClick(dateObj));
        }

        calendarGrid.appendChild(dayCell);
    }
}

// Tratar clique em um dia válido do calendário
function handleDayClick(clickedDate) {
    if (!checkinDate || (checkinDate && checkoutDate)) {
        // Primeiro clique ou reset de seleção
        checkinDate = clickedDate;
        checkoutDate = null;
        showToast('Check-in selecionado. Agora selecione a data de check-out.');
    } else {
        // Segundo clique (seleção de checkout)
        if (clickedDate <= checkinDate) {
            // Se clicar antes do checkin, redefine o checkin
            checkinDate = clickedDate;
            showToast('Data de check-in atualizada. Escolha o check-out.');
        } else {
            // Validar se há conflitos (reservas bloqueadas) dentro do período selecionado
            let hasConflict = false;
            let temp = new Date(checkinDate);
            while (temp < clickedDate) {
                if (bookedDates.has(formatISODate(temp))) {
                    hasConflict = true;
                    break;
                }
                temp.setDate(temp.getDate() + 1);
            }

            if (hasConflict) {
                showToast('O período contém dias já reservados! Por favor, selecione outro intervalo.');
                checkinDate = clickedDate;
                checkoutDate = null;
            } else {
                checkoutDate = clickedDate;
                showToast('Período de estadia definido com sucesso!');
            }
        }
    }
    
    renderCalendar();
    updatePriceSummary();
}

// Atualiza o resumo visual de preço das diárias
function updatePriceSummary() {
    if (checkinDate && checkoutDate) {
        const diffTime = Math.abs(checkoutDate - checkinDate);
        const nights = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        const totalPrice = nights * dailyRate;

        summaryNights.textContent = `${nights} noite(s)`;
        summaryTotal.textContent = `R$ ${totalPrice.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
        priceSummary.style.display = 'block';
        btnReserve.disabled = false;
    } else {
        priceSummary.style.display = 'none';
        btnReserve.disabled = true;
    }
}

// Habilitar submissão se o formulário for minimamente preenchido
function setupFormValidation() {
    const inputs = ['guest_name', 'guest_whatsapp', 'guest_email'];
    inputs.forEach(id => {
        document.getElementById(id).addEventListener('input', () => {
            // O botão só habilita se tiver datas + campos preenchidos
            const name = document.getElementById('guest_name').value.trim();
            const whatsapp = document.getElementById('guest_whatsapp').value.trim();
            const email = document.getElementById('guest_email').value.trim();
            
            btnReserve.disabled = !(checkinDate && checkoutDate && name && whatsapp && email);
        });
    });
}

// Evento de envio do formulário de reserva
reservationForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('guest_name').value.trim();
    const whatsapp = document.getElementById('guest_whatsapp').value.trim();
    const email = document.getElementById('guest_email').value.trim();

    if (!checkinDate || !checkoutDate || !name || !whatsapp || !email) {
        showToast('Por favor, preencha todos os dados e selecione o período.');
        return;
    }

    const diffTime = Math.abs(checkoutDate - checkinDate);
    const nights = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    const totalPrice = nights * dailyRate;

    const payload = {
        guest_name: name,
        guest_whatsapp: whatsapp,
        guest_email: email,
        checkin_date: formatISODate(checkinDate),
        checkout_date: formatISODate(checkoutDate),
        total_price: totalPrice
    };

    // Estilo de carregamento no botão
    btnReserve.disabled = true;
    const originalText = btnReserve.innerHTML;
    btnReserve.innerHTML = '<div class="spinner"></div> Processando...';

    try {
        const response = await fetch('/api/reservar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            // Sucesso absoluto! Exibir ticket de reserva
            document.getElementById('ticket-guest-name').textContent = result.booking.guest_name;
            document.getElementById('ticket-period').textContent = `${result.booking.checkin_date} a ${result.booking.checkout_date}`;
            document.getElementById('ticket-nights').textContent = `${nights} noite(s)`;
            document.getElementById('ticket-total').textContent = `R$ ${totalPrice.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
            
            const pixPayloadElement = document.getElementById('pix-payload');
            pixPayloadElement.textContent = result.pix_code;
            
            // Botão copiar Pix
            document.getElementById('btn-copy-pix').onclick = () => {
                navigator.clipboard.writeText(result.pix_code);
                showToast('Código Pix copiado para a área de transferência!');
            };

            // Link do WhatsApp
            document.getElementById('btn-send-whatsapp').setAttribute('href', result.whatsapp_link);

            // Trocar tela
            bookingFlow.style.display = 'none';
            successFlow.style.display = 'block';
            successFlow.scrollIntoView({ behavior: 'smooth' });
        } else {
            showToast(result.error || 'Ocorreu um erro ao processar a reserva.');
            btnReserve.disabled = false;
            btnReserve.innerHTML = originalText;
        }
    } catch (err) {
        console.error(err);
        showToast('Erro de conexão com o servidor. Tente novamente mais tarde.');
        btnReserve.disabled = false;
        btnReserve.innerHTML = originalText;
    }
});
