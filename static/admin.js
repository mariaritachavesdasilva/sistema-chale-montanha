// Elementos do DOM
const adminLoginSection = document.getElementById('admin-login-section');
const adminDashboardSection = document.getElementById('admin-dashboard-section');
const adminLoginForm = document.getElementById('admin-login-form');
const adminTokenInput = document.getElementById('admin_token');
const reservasTbody = document.getElementById('reservas-tbody');
const btnLogout = document.getElementById('btn-logout');
const toastMessage = document.getElementById('toast-message');

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    const savedToken = sessionStorage.getItem('admin_token');
    if (savedToken) {
        verifyAndLoadDashboard(savedToken);
    }
});

// Toast Notificações
function showToast(message, duration = 3000) {
    toastMessage.textContent = message;
    toastMessage.style.display = 'block';
    setTimeout(() => {
        toastMessage.style.display = 'none';
    }, duration);
}

// Formulário de Login Administrativo
adminLoginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const token = adminTokenInput.value.trim();
    if (token) {
        verifyAndLoadDashboard(token);
    }
});

// Botão de Logout
btnLogout.addEventListener('click', () => {
    sessionStorage.removeItem('admin_token');
    adminDashboardSection.style.display = 'none';
    adminLoginSection.style.display = 'block';
    showToast('Sessão encerrada com sucesso.');
});

// Validar o Token e Carregar Dados do Painel
async function verifyAndLoadDashboard(token) {
    try {
        const response = await fetch('/api/admin/reservas', {
            method: 'GET',
            headers: {
                'X-Admin-Token': token
            }
        });

        if (response.ok) {
            // Guardar token na sessão
            sessionStorage.setItem('admin_token', token);
            
            // Ocultar login e mostrar dashboard
            adminLoginSection.style.display = 'none';
            adminDashboardSection.style.display = 'block';
            
            const data = await response.json();
            renderReservasTable(data);
        } else if (response.status === 401) {
            showToast('Token inválido ou não autorizado.');
            sessionStorage.removeItem('admin_token');
        } else {
            showToast('Erro ao carregar o painel administrativo.');
        }
    } catch (error) {
        console.error(error);
        showToast('Erro de conexão ao acessar o servidor.');
    }
}

// Renderizar linhas da tabela de reservas
function renderReservasTable(reservas) {
    reservasTbody.innerHTML = '';
    
    if (reservas.length === 0) {
        reservasTbody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: rgba(255,255,255,0.4);">Nenhuma reserva registrada no sistema.</td></tr>';
        return;
    }

    reservas.forEach(res => {
        const tr = document.createElement('tr');
        
        // Formatar Moeda
        const formattedPrice = `R$ ${res.total_price.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
        
        // Badge de Status
        const statusClass = `status-${res.status}`;
        
        // Gerar botões dependendo do status atual
        let actionButtons = '';
        if (res.status === 'pendente') {
            actionButtons = `
                <button class="btn-action btn-confirm" onclick="updateStatus(${res.id}, 'confirmada')">Confirmar</button>
                <button class="btn-action btn-cancel" onclick="updateStatus(${res.id}, 'cancelada')">Cancelar</button>
            `;
        } else if (res.status === 'confirmada') {
            actionButtons = `
                <button class="btn-action btn-cancel" onclick="updateStatus(${res.id}, 'cancelada')">Cancelar</button>
            `;
        } else if (res.status === 'cancelada') {
            actionButtons = `
                <button class="btn-action btn-confirm" onclick="updateStatus(${res.id}, 'confirmada')">Reativar</button>
            `;
        }

        tr.innerHTML = `
            <td>#${res.id}</td>
            <td><strong>${escapeHTML(res.guest_name)}</strong></td>
            <td><a href="https://wa.me/55${res.guest_whatsapp}" target="_blank" style="color: #25d366; text-decoration: none;">${res.guest_whatsapp}</a></td>
            <td>${escapeHTML(res.guest_email)}</td>
            <td>${res.checkin_date}</td>
            <td>${res.checkout_date}</td>
            <td style="font-weight: 600; color: var(--gold);">${formattedPrice}</td>
            <td><span class="status-badge ${statusClass}">${res.status}</span></td>
            <td style="text-align: center;">${actionButtons}</td>
        `;
        
        reservasTbody.appendChild(tr);
    });
}

// Utilitário para evitar XSS básico
function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}

// Atualizar status de uma reserva
async function updateStatus(id, newStatus) {
    const token = sessionStorage.getItem('admin_token');
    if (!token) return;

    if (!confirm(`Tem certeza que deseja atualizar a reserva #${id} para '${newStatus}'?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/admin/reservas/${id}/status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Admin-Token': token
            },
            body: JSON.stringify({ status: newStatus })
        });

        const result = await response.json();
        
        if (response.ok) {
            showToast(`Reserva #${id} atualizada com sucesso.`);
            // Recarregar os dados
            verifyAndLoadDashboard(token);
        } else {
            showToast(result.error || 'Erro ao atualizar status.');
        }
    } catch (err) {
        console.error(err);
        showToast('Erro de conexão ao enviar atualização.');
    }
}
