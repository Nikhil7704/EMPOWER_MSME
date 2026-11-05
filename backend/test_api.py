import os
import sys

# Ensure backend root in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_endpoints():
    print("[*] Running EmpowerMSME FastAPI Automated Integration Tests...\n")
    
    # 1. Health check & Root
    r = client.get("/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    print("[PASS] GET /health -> 200 OK")

    # 2. Auth Login
    r = client.post("/api/auth/login", json={"email": "business@demo.com", "password": "demo1234"})
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json()["token"]
    user_id = r.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    print("[PASS] POST /api/auth/login -> 200 OK (JWT issued)")

    # 3. Auth Me
    r = client.get("/api/auth/me", headers=headers)
    assert r.status_code == 200, f"Me endpoint failed: {r.text}"
    print("[PASS] GET /api/auth/me -> 200 OK")

    # 4. Campaigns List
    r = client.get("/api/campaigns")
    assert r.status_code == 200, f"Campaigns failed: {r.text}"
    camps = r.json()["data"]
    assert len(camps) > 0, "No campaigns found"
    camp_id = camps[0]["id"]
    print(f"[PASS] GET /api/campaigns -> 200 OK ({len(camps)} campaigns returned)")

    # 5. Campaign Investment
    r = client.post("/api/campaigns/invest", json={"campaignId": camp_id, "amount": 25000}, headers=headers)
    assert r.status_code == 200, f"Invest failed: {r.text}"
    print("[PASS] POST /api/campaigns/invest -> 200 OK")

    # 6. Loans List & Create
    r = client.get("/api/loans")
    assert r.status_code == 200, f"Loans list failed: {r.text}"
    print(f"[PASS] GET /api/loans -> 200 OK")

    r = client.post("/api/loans", json={"amount": 400000, "tenure": 12, "interestRate": 10.5}, headers=headers)
    assert r.status_code == 200, f"Loan create failed: {r.text}"
    loan_id = r.json()["data"]["id"]
    print(f"[PASS] POST /api/loans -> 200 OK (Loan ID: {loan_id[:8]}...)")

    # 7. Repayments Schedule
    r = client.get(f"/api/repayments?loanId={loan_id}")
    assert r.status_code == 200, f"Repayments failed: {r.text}"
    print("[PASS] GET /api/repayments -> 200 OK")

    # 8. Credit Scoring Engine
    r = client.get("/api/credit/evaluate")
    assert r.status_code == 200
    print("[PASS] GET /api/credit/evaluate -> 200 OK (Metadata)")

    eval_payload = {
        "annualRevenue": 3500000,
        "netProfitMargin": 18,
        "cashFlowVariance": 22,
        "existingDebt": 400000,
        "repaymentHistory": 88,
        "businessAge": 4,
        "gstFilingScore": 92,
        "industryRiskLevel": "low"
    }
    r = client.post("/api/credit/evaluate", json=eval_payload, headers=headers)
    assert r.status_code == 200
    data = r.json()["data"]
    print(f"[PASS] POST /api/credit/evaluate -> 200 OK (Score: {data['creditScore']}, Tier: {data['eligibilityTier']})")

    # 9. Lending Circles
    r = client.get("/api/lending-circles")
    assert r.status_code == 200
    print("[PASS] GET /api/lending-circles -> 200 OK")

    # 10. Analytics
    r = client.get(f"/api/analytics/business?userId={user_id}")
    assert r.status_code == 200
    print("[PASS] GET /api/analytics/business -> 200 OK")

    r = client.get("/api/analytics/user")
    assert r.status_code == 200
    print("[PASS] GET /api/analytics/user -> 200 OK")

    # 11. Admin Endpoints
    r = client.get("/api/admin/users")
    assert r.status_code == 200
    print(f"[PASS] GET /api/admin/users -> 200 OK ({len(r.json()['data'])} users)")

    r = client.get("/api/admin/businesses")
    assert r.status_code == 200
    print(f"[PASS] GET /api/admin/businesses -> 200 OK")

    # 12. Chat & RAG
    r = client.get("/api/rag")
    assert r.status_code == 200
    print("[PASS] GET /api/rag -> 200 OK (RAG Status)")

    r = client.post("/api/chat", json={"message": "What is MUDRA loan and what are the categories?"})
    assert r.status_code == 200
    chat_resp = r.json()
    print(f"[PASS] POST /api/chat -> 200 OK (Model: {chat_resp['model']})")

    print("\n[SUCCESS] ALL 12 INTEGRATION TESTS PASSED! FastAPI backend is 100% operational.")

if __name__ == "__main__":
    test_endpoints()
