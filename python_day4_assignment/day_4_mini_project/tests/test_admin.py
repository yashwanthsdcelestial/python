"""5 admin tests: view all loans, approve, reject, re-review error, non-admin 403."""
from tests.conftest import auth_headers, register_and_login


def _create_loan(client, user_token, payload=None):
    payload = payload or {
        "amount": 300000,
        "purpose": "personal",
        "tenure_months": 60,
        "employment_status": "employed",
    }
    resp = client.post("/loans", json=payload, headers=auth_headers(user_token))
    assert resp.status_code == 201
    return resp.json()["id"]


def test_admin_views_all_loans(client, user_token, admin_token):
    _create_loan(client, user_token)
    resp = client.get("/admin/loans", headers=auth_headers(admin_token))
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) == 1


def test_admin_approves_loan(client, user_token, admin_token):
    loan_id = _create_loan(client, user_token)

    resp = client.patch(
        f"/admin/loans/{loan_id}/review",
        json={"status": "approved", "admin_remarks": "Good income-to-loan ratio. Approved."},
        headers=auth_headers(admin_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "approved"
    assert body["reviewed_by"] == "admin"
    assert body["admin_remarks"] is not None


def test_admin_rejects_loan(client, user_token, admin_token):
    loan_id = _create_loan(client, user_token)

    resp = client.patch(
        f"/admin/loans/{loan_id}/review",
        json={"status": "rejected", "admin_remarks": "Insufficient income for requested amount."},
        headers=auth_headers(admin_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "rejected"
    assert body["reviewed_by"] == "admin"


def test_admin_cannot_re_review(client, user_token, admin_token):
    loan_id = _create_loan(client, user_token)

    # First review
    client.patch(
        f"/admin/loans/{loan_id}/review",
        json={"status": "approved", "admin_remarks": "Looks good to me, approved."},
        headers=auth_headers(admin_token),
    )

    # Attempt second review on the same loan
    resp = client.patch(
        f"/admin/loans/{loan_id}/review",
        json={"status": "rejected", "admin_remarks": "Changed my mind, rejecting now."},
        headers=auth_headers(admin_token),
    )
    assert resp.status_code == 422
    assert resp.json()["error"] == "InvalidLoanReviewError"


def test_non_admin_cannot_access_admin_endpoint(client, user_token):
    resp = client.get("/admin/loans", headers=auth_headers(user_token))
    assert resp.status_code == 403
    assert resp.json()["error"] == "ForbiddenError"