import os
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template

# Configuração de caminhos absolutos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'chalet.db')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

# Chave secreta de administração
ADMIN_TOKEN = os.environ.get("CHALET_ADMIN_TOKEN", "admin_secret_token_2026")

def init_db():
    """Inicializa o banco de dados SQLite com a tabela reservas conforme SCHEMA.md."""
    print(f"[*] Inicializando banco de dados em: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_name TEXT NOT NULL,
            guest_whatsapp TEXT NOT NULL,
            guest_email TEXT NOT NULL,
            checkin_date TEXT NOT NULL,
            checkout_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pendente',
            total_price REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_dates_between(start_str, end_str):
    """Retorna uma lista de strings de data ISO YYYY-MM-DD de start_str (inclusive) a end_str (exclusive)."""
    start = datetime.strptime(start_str, "%Y-%m-%d")
    end = datetime.strptime(end_str, "%Y-%m-%d")
    dates = []
    curr = start
    while curr < end:
        dates.append(curr.strftime("%Y-%m-%d"))
        curr += timedelta(days=1)
    return dates

@app.route('/')
def home():
    """Serviço do Frontend - Home."""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Serviço do Frontend - Painel do Anfitrião."""
    return render_template('admin.html')

@app.route('/api/disponibilidade', methods=['GET'])
def api_disponibilidade():
    """GET /api/disponibilidade: Retorna a lista de todas as datas já ocupadas."""
    print("[DISPONIBILIDADE] Solicitando disponibilidade do chale...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT checkin_date, checkout_date FROM reservas WHERE status != 'cancelada'")
    reservas = cursor.fetchall()
    conn.close()

    dates_booked = set()
    for res in reservas:
        booked_range = get_dates_between(res['checkin_date'], res['checkout_date'])
        dates_booked.update(booked_range)

    print(f"[DISPONIBILIDADE] Total de dias ocupados encontrados: {len(dates_booked)}")
    return jsonify({"dates_booked": sorted(list(dates_booked))}), 200

@app.route('/api/reservar', methods=['POST'])
def api_reservar():
    """POST /api/reservar: Cria uma reserva após validação e prevenção de overbooking."""
    data = request.json or {}
    guest_name = data.get("guest_name")
    guest_whatsapp = data.get("guest_whatsapp")
    guest_email = data.get("guest_email")
    checkin_date = data.get("checkin_date")
    checkout_date = data.get("checkout_date")
    total_price = data.get("total_price")

    # Validação de dados presentes
    if not all([guest_name, guest_whatsapp, guest_email, checkin_date, checkout_date, total_price]):
        return jsonify({"error": "Preencha todos os campos obrigatórios."}), 400

    # Limpeza do WhatsApp (manter apenas dígitos)
    guest_whatsapp = "".join(filter(str.isdigit, str(guest_whatsapp)))

    print(f"[RESERVA] Verificando disponibilidade para {guest_name} no periodo: {checkin_date} a {checkout_date}...")

    # Validação de Datas (checkout posterior ao checkin)
    try:
        start_date = datetime.strptime(checkin_date, "%Y-%m-%d")
        end_date = datetime.strptime(checkout_date, "%Y-%m-%d")
        if start_date >= end_date:
            print(f"[VALIDACAO] RN01 Violada: Check-out ({checkout_date}) nao e posterior ao check-in ({checkin_date})")
            return jsonify({"error": "A data de check-out deve ser posterior à data de check-in."}), 400
    except ValueError:
        return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD."}), 400

    # Validação de transação e prevenção de Overbooking (ACID)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Início imediato da transação de escrita para evitar concorrência (Overbooking)
        cursor.execute("BEGIN IMMEDIATE")
        
        cursor.execute("""
            SELECT COUNT(*) FROM reservas 
            WHERE status != 'cancelada' 
              AND checkin_date < ? 
              AND ? < checkout_date
        """, (checkout_date, checkin_date))
        conflitos = cursor.fetchone()[0]

        if conflitos > 0:
            print(f"[CONFLITO] Conflito de datas detectado para {checkin_date} a {checkout_date}!")
            conn.rollback()
            return jsonify({"error": "Datas já reservadas por outro hóspede (Proteção contra overbooking)."}), 409

        cursor.execute("""
            INSERT INTO reservas (guest_name, guest_whatsapp, guest_email, checkin_date, checkout_date, total_price, status)
            VALUES (?, ?, ?, ?, ?, ?, 'pendente')
        """, (guest_name, guest_whatsapp, guest_email, checkin_date, checkout_date, total_price))
        booking_id = cursor.lastrowid
        
        conn.commit()
        print(f"[SUCESSO] Reserva temporaria criada com sucesso para {guest_name} (ID: {booking_id}).")
    except Exception as e:
        conn.rollback()
        print(f"[ERRO] Erro no banco de dados: {e}")
        return jsonify({"error": "Erro interno ao processar a reserva."}), 500
    finally:
        conn.close()

    # Criação do Pix Simulado e Link de WhatsApp
    pix_key = "chaletpixkey@merchant.com"
    pix_payload = f"00020101021226830014br.gov.bcb.pix2532{pix_key}5204000053039865407{total_price:.2f}5802BR5915Chalet Montanha6009Sao Paulo62070503***6304abcd"
    
    # URL encoded WhatsApp message link
    wa_message = f"Olá! Acabei de registrar uma reserva para o Chalé Montanha de {checkin_date} a {checkout_date}. Segue comprovante do Pix no valor de R$ {total_price:.2f}."
    from urllib.parse import quote
    whatsapp_link = f"https://wa.me/55{guest_whatsapp}?text={quote(wa_message)}"

    return jsonify({
        "message": "Reserva pré-aprovada! Aguardando confirmação de pagamento.",
        "booking": {
            "id": booking_id,
            "guest_name": guest_name,
            "guest_whatsapp": guest_whatsapp,
            "guest_email": guest_email,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "total_price": total_price,
            "status": "pendente"
        },
        "pix_code": pix_payload,
        "whatsapp_link": whatsapp_link
    }), 201

@app.route('/api/admin/reservas', methods=['GET'])
def api_admin_reservas():
    """GET /api/admin/reservas: Retorna a lista completa de reservas (protegida por Header X-Admin-Token)."""
    token = request.headers.get("X-Admin-Token")
    if token != ADMIN_TOKEN:
        print("[ADMIN] Tentativa de acesso nao autorizada ao painel admin!")
        return jsonify({"error": "Acesso não autorizado."}), 401

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservas ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    reservas = [dict(row) for row in rows]
    return jsonify(reservas), 200

@app.route('/api/admin/reservas/<int:booking_id>/status', methods=['POST'])
def api_admin_update_status(booking_id):
    """POST /api/admin/reservas/<id>/status: Atualiza o status da reserva (confirmada, cancelada, pendente)."""
    token = request.headers.get("X-Admin-Token")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "Acesso não autorizado."}), 401

    data = request.json or {}
    new_status = data.get("status")
    if new_status not in ["pendente", "confirmada", "cancelada"]:
        return jsonify({"error": "Status inválido."}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE reservas SET status = ? WHERE id = ?", (new_status, booking_id))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()

    if rows_affected == 0:
        return jsonify({"error": "Reserva não encontrada."}), 404

    print(f"[STATUS] Reserva ID {booking_id} atualizada para o status: {new_status}")
    return jsonify({"message": f"Status da reserva {booking_id} atualizado com sucesso para {new_status}."}), 200

# Inicialização automática do Banco
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
