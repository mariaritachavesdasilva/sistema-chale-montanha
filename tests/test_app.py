import os
import unittest
import tempfile
import sqlite3
import json
import app

class ChaletAppTestCase(unittest.TestCase):
    def setUp(self):
        """Arrange: Configurar um banco de dados de teste isolado e o cliente Flask."""
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.DB_PATH = self.db_path
        app.init_db()
        
        self.client = app.app.test_client()
        app.app.config['TESTING'] = True
        self.admin_token = "admin_secret_token_2026"

    def tearDown(self):
        """Limpeza pós-teste."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_basic_booking_success(self):
        """Teste de reserva básica bem-sucedida."""
        # Arrange
        payload = {
            "guest_name": "Carlos Silva",
            "guest_whatsapp": "11999999999",
            "guest_email": "carlos@email.com",
            "checkin_date": "2026-06-20",
            "checkout_date": "2026-06-25",
            "total_price": 1250.00
        }

        # Act
        response = self.client.post(
            '/api/reservar',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['booking']['guest_name'], "Carlos Silva")
        self.assertEqual(data['booking']['status'], "pendente")
        self.assertIn("pix_code", data)
        self.assertIn("whatsapp_link", data)

    def test_invalid_checkout_date(self):
        """Teste de validação de data: check-out anterior ou igual ao check-in (RN01)."""
        # Arrange
        payload = {
            "guest_name": "Carlos Silva",
            "guest_whatsapp": "11999999999",
            "guest_email": "carlos@email.com",
            "checkin_date": "2026-06-20",
            "checkout_date": "2026-06-20",
            "total_price": 0.00
        }

        # Act
        response = self.client.post(
            '/api/reservar',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)

    def test_overbooking_conflict_middle(self):
        """Teste de Overbooking: conflito total dentro de um período já reservado."""
        # Arrange
        # 1. Inserir reserva existente (10 a 15 de Junho)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservas (guest_name, guest_whatsapp, guest_email, checkin_date, checkout_date, total_price, status)
            VALUES ('Hóspede Existente', '11988888888', 'existente@email.com', '2026-06-10', '2026-06-15', 1250.00, 'confirmada')
        """)
        conn.commit()
        conn.close()

        # 2. Payload conflitante: 12 a 14 de Junho (meio do período)
        payload = {
            "guest_name": "Carlos Conflito",
            "guest_whatsapp": "11999999999",
            "guest_email": "conflito@email.com",
            "checkin_date": "2026-06-12",
            "checkout_date": "2026-06-14",
            "total_price": 500.00
        }

        # Act
        response = self.client.post(
            '/api/reservar',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        self.assertEqual(response.status_code, 409)

    def test_overbooking_conflict_partial_start(self):
        """Teste de Overbooking: conflito parcial no início da reserva existente."""
        # Arrange
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservas (guest_name, guest_whatsapp, guest_email, checkin_date, checkout_date, total_price, status)
            VALUES ('Hóspede Existente', '11988888888', 'existente@email.com', '2026-06-10', '2026-06-15', 1250.00, 'confirmada')
        """)
        conn.commit()
        conn.close()

        # Payload conflitante: 08 a 12 de Junho
        payload = {
            "guest_name": "Carlos Conflito",
            "guest_whatsapp": "11999999999",
            "guest_email": "conflito@email.com",
            "checkin_date": "2026-06-08",
            "checkout_date": "2026-06-12",
            "total_price": 1000.00
        }

        # Act
        response = self.client.post(
            '/api/reservar',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        self.assertEqual(response.status_code, 409)

    def test_overbooking_conflict_partial_end(self):
        """Teste de Overbooking: conflito parcial no final da reserva existente."""
        # Arrange
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservas (guest_name, guest_whatsapp, guest_email, checkin_date, checkout_date, total_price, status)
            VALUES ('Hóspede Existente', '11988888888', 'existente@email.com', '2026-06-10', '2026-06-15', 1250.00, 'confirmada')
        """)
        conn.commit()
        conn.close()

        # Payload conflitante: 13 a 18 de Junho
        payload = {
            "guest_name": "Carlos Conflito",
            "guest_whatsapp": "11999999999",
            "guest_email": "conflito@email.com",
            "checkin_date": "2026-06-13",
            "checkout_date": "2026-06-18",
            "total_price": 1250.00
        }

        # Act
        response = self.client.post(
            '/api/reservar',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        self.assertEqual(response.status_code, 409)

    def test_overbooking_no_conflict_adjacent(self):
        """Sem conflito: nova reserva inicia no mesmo dia do checkout da anterior."""
        # Arrange
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservas (guest_name, guest_whatsapp, guest_email, checkin_date, checkout_date, total_price, status)
            VALUES ('Hóspede Existente', '11988888888', 'existente@email.com', '2026-06-10', '2026-06-15', 1250.00, 'confirmada')
        """)
        conn.commit()
        conn.close()

        # Payload não conflitante: 15 a 20 de Junho (dia 15 é checkout da anterior)
        payload = {
            "guest_name": "Hóspede Seguinte",
            "guest_whatsapp": "11977777777",
            "guest_email": "seguinte@email.com",
            "checkin_date": "2026-06-15",
            "checkout_date": "2026-06-20",
            "total_price": 1250.00
        }

        # Act
        response = self.client.post(
            '/api/reservar',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        self.assertEqual(response.status_code, 201)

    def test_admin_auth_and_status_update(self):
        """Teste de autenticação admin e atualização de status."""
        # Arrange: inserir reserva pendente
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservas (guest_name, guest_whatsapp, guest_email, checkin_date, checkout_date, total_price, status)
            VALUES ('João das Neves', '11966666666', 'neves@email.com', '2026-06-25', '2026-06-28', 750.00, 'pendente')
        """)
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Act 1: Get reservas sem token
        response_get_fail = self.client.get('/api/admin/reservas')
        # Assert 1
        self.assertEqual(response_get_fail.status_code, 401)

        # Act 2: Get reservas com token correto
        response_get_ok = self.client.get(
            '/api/admin/reservas',
            headers={"X-Admin-Token": self.admin_token}
        )
        data_get = json.loads(response_get_ok.data)
        # Assert 2
        self.assertEqual(response_get_ok.status_code, 200)
        self.assertEqual(len(data_get), 1)

        # Act 3: Atualizar status para confirmada
        response_update = self.client.post(
            f'/api/admin/reservas/{booking_id}/status',
            data=json.dumps({"status": "confirmada"}),
            content_type='application/json',
            headers={"X-Admin-Token": self.admin_token}
        )
        data_update = json.loads(response_update.data)
        # Assert 3
        self.assertEqual(response_update.status_code, 200)
        self.assertIn("confirmada", data_update['message'])

        # Act 4: Verificar se persistiu
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM reservas WHERE id = ?", (booking_id,))
        new_status = cursor.fetchone()[0]
        conn.close()
        # Assert 4
        self.assertEqual(new_status, "confirmada")

if __name__ == '__main__':
    unittest.main()
