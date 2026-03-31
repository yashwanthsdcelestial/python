"""5 loan tests: apply success, amount exceeds limit, max pending, list my loans, single detail."""
from tests.conftest import auth_headers


def test_apply_loan_success(client, user_token, loan_payload):
    resp = client.post("/loans", json=loan_payload, headers=auth_headers(user_token))
    assert resp.status_code == 201
    body = resp.json()
    assert body["amount"] == 500000
    assert body["status"] == "pending"
    assert body["purpose"] == "home"


def test_apply_loan_amount_exceeds_limit(client, user_token):
    resp = client.post("/loans", json={
        "amount": 2000000,          # over ₹10,00,000 limit
        "purpose": "personal",
        "tenure_months": 60,
        "employment_status": "employed",
    }, headers=auth_headers(user_token))
    assert resp.status_code == 422


def test_apply_loan_max_pending(client, user_token, loan_payload):
    # Submit 3 pending loans successfully
    for _ in range(3):
        r = client.post("/loans", json=loan_payload, headers=auth_headers(user_token))
        assert r.status_code == 201

    # 4th should be blocked
    resp = client.post("/loans", json=loan_payload, headers=auth_headers(user_token))
    assert resp.status_code == 422
    assert resp.json()["error"] == "MaxPendingLoansError"


def test_get_my_loans(client, user_token, loan_payload):
    client.post("/loans", json=loan_payload, headers=auth_headers(user_token))
    resp = client.get("/loans/my", headers=auth_headers(user_token))
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["status"] == "pending"


def test_get_single_loan_detail(client, user_token, loan_payload):
    create_resp = client.post("/loans", json=loan_payload, headers=auth_headers(user_token))
    loan_id = create_resp.json()["id"]

    resp = client.get(f"/loans/my/{loan_id}", headers=auth_headers(user_token))
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == loan_id
    assert body["amount"] == 500000