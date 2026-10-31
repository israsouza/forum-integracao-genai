"""Esqueleto pytest dos cenários INT-xx. Requer um ambiente com o Serviço de Pagamentos
mockável (ex.: WireMock em PAYMENTS_MOCK_URL). Execute: BASE_URL=http://localhost:8080 pytest -v
"""
import os
import uuid

import pytest
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
MOCK_URL = os.getenv("PAYMENTS_MOCK_URL", "http://localhost:8089")

ORDER = {
    "customer_id": "c1",
    "items": [{"sku": "A1", "qty": 2}],
    "payment_method": "CARD",
}


def stub_payments(status=200, body=None, delay_ms=0):
    """Configura o mock do serviço de pagamentos (formato WireMock)."""
    requests.post(
        f"{MOCK_URL}/__admin/mappings",
        json={
            "request": {"method": "POST", "url": "/payments"},
            "response": {"status": status, "jsonBody": body, "fixedDelayMilliseconds": delay_ms},
        },
        timeout=5,
    ).raise_for_status()


@pytest.fixture(autouse=True)
def reset_mock():
    requests.delete(f"{MOCK_URL}/__admin/mappings", timeout=5)
    requests.delete(f"{MOCK_URL}/__admin/requests", timeout=5)


def payments_calls():
    r = requests.get(f"{MOCK_URL}/__admin/requests", timeout=5).json()
    return [x for x in r["requests"] if x["request"]["url"] == "/payments"]


def test_int01_pedido_pago():
    stub_payments(200, {"payment_id": "p1", "status": "APPROVED"})
    r = requests.post(f"{BASE_URL}/orders", json=ORDER, timeout=10)
    assert r.status_code == 201
    oid = r.json()["order_id"]
    assert requests.get(f"{BASE_URL}/orders/{oid}", timeout=5).json()["status"] == "PAID"


def test_int02_pagamento_recusado():
    stub_payments(200, {"payment_id": "p2", "status": "DECLINED"})
    oid = requests.post(f"{BASE_URL}/orders", json=ORDER, timeout=10).json()["order_id"]
    assert requests.get(f"{BASE_URL}/orders/{oid}", timeout=5).json()["status"] == "PAYMENT_FAILED"


def test_int03_timeout():
    stub_payments(200, {"status": "APPROVED"}, delay_ms=30000)
    assert requests.post(f"{BASE_URL}/orders", json=ORDER, timeout=40).status_code == 504


def test_int04_pagamentos_indisponivel():
    stub_payments(503, {"error": "unavailable"})
    assert requests.post(f"{BASE_URL}/orders", json=ORDER, timeout=10).status_code == 502


def test_int05_idempotencia():
    stub_payments(200, {"payment_id": "p5", "status": "APPROVED"})
    h = {"Idempotency-Key": str(uuid.uuid4())}
    a = requests.post(f"{BASE_URL}/orders", json=ORDER, headers=h, timeout=10).json()
    b = requests.post(f"{BASE_URL}/orders", json=ORDER, headers=h, timeout=10).json()
    assert a["order_id"] == b["order_id"]
    assert len(payments_calls()) == 1


def test_int06_contrato_sem_status():
    stub_payments(200, {})
    assert requests.post(f"{BASE_URL}/orders", json=ORDER, timeout=10).status_code == 502


def test_int07_status_desconhecido():
    stub_payments(200, {"status": "PENDING_REVIEW"})
    r = requests.post(f"{BASE_URL}/orders", json=ORDER, timeout=10)
    if r.status_code == 201:
        oid = r.json()["order_id"]
        assert requests.get(f"{BASE_URL}/orders/{oid}", timeout=5).json()["status"] != "PAID"


def test_int09_pedido_inexistente():
    assert requests.get(f"{BASE_URL}/orders/inexistente", timeout=5).status_code == 404
