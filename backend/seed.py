import os
import sys
from datetime import datetime, timedelta

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.models import (
    User,
    BusinessProfile,
    Campaign,
    Investment,
    Loan,
    RepaymentLedger,
    LendingCircle,
    LendingCircleMember,
    AuditLog
)

def seed_database():
    print("[*] Initializing EmpowerMSME database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).count() > 0:
            print("[!] Database already contains records. Skipping seed.")
            return

        print("[*] Seeding initial users and roles...")
        pw_hash = get_password_hash("demo1234")

        # 1. Admin
        admin = User(
            email="admin@demo.com",
            password_hash=pw_hash,
            role="ADMIN",
            kyc_status="VERIFIED"
        )
        db.add(admin)

        # 2. Business User
        biz_user = User(
            email="business@demo.com",
            password_hash=pw_hash,
            role="BUSINESS",
            kyc_status="VERIFIED"
        )
        db.add(biz_user)
        db.flush()

        biz_profile = BusinessProfile(
            user_id=biz_user.id,
            name="GreenLeaf Organics",
            sector="Sustainable Agriculture",
            location="Pune, Maharashtra",
            udyam_id="UDYAM-MH-26-0012345",
            employees=18,
            business_age=4.5,
            website="https://greenleaf.example.com",
            description="Tech-enabled organic farm-to-table supply chain aggregator partnering with 250+ smallholder farmers across western Maharashtra.",
            funding_goal=1500000.0,
            credit_score=742
        )
        db.add(biz_profile)
        db.flush()

        # 3. Investor User
        investor = User(
            email="investor@demo.com",
            password_hash=pw_hash,
            role="INVESTOR",
            kyc_status="VERIFIED"
        )
        db.add(investor)
        db.flush()

        print("Seeding campaigns...")
        camp1 = Campaign(
            business_id=biz_profile.id,
            title="Cold Storage & Solar Micro-Grid Expansion",
            description="Establishing 3 distributed off-grid solar cold storage units in Junnar and Nashik to eliminate post-harvest perishability loss.",
            goal=1500000.0,
            raised=850000.0,
            risk_rating="Low",
            roi=14.5,
            repayment_model="Revenue Share (4.5% gross sales)",
            status="active"
        )
        camp2 = Campaign(
            business_id=biz_profile.id,
            title="Drip Irrigation Automation IoT Kits",
            description="Supplying 150 smallholder farmers with automated IoT soil moisture valves to cut water usage by 40%.",
            goal=800000.0,
            raised=320000.0,
            risk_rating="Medium",
            roi=12.0,
            repayment_model="Fixed EMI + Bonus Royalty",
            status="active"
        )
        db.add_all([camp1, camp2])
        db.flush()

        print("Seeding investments...")
        inv1 = Investment(
            campaign_id=camp1.id,
            investor_id=investor.id,
            amount=150000.0,
            status="active"
        )
        inv2 = Investment(
            campaign_id=camp2.id,
            investor_id=investor.id,
            amount=50000.0,
            status="active"
        )
        db.add_all([inv1, inv2])

        print("Seeding loans & repayment ledgers...")
        loan1 = Loan(
            business_id=biz_profile.id,
            amount=600000.0,
            platform_fee=12000.0,
            interest_rate=10.5,
            tenure_months=12,
            status="disbursed",
            bank_name="State Bank of India",
            account_num="987654321012",
            ifsc="SBIN0001234"
        )
        db.add(loan1)
        db.flush()

        for month in range(1, 13):
            is_past = month <= 2
            due_dt = datetime.utcnow() + timedelta(days=30 * (month - 2))
            ledger = RepaymentLedger(
                loan_id=loan1.id,
                due_date=due_dt,
                amount_due=52500.0,
                amount_paid=52500.0 if is_past else 0.0,
                status="paid" if is_past else "pending",
                paid_date=due_dt if is_past else None
            )
            db.add(ledger)

        print("Seeding lending circles...")
        circle = LendingCircle(
            name="Western Agri-Tech Mutual Circle",
            contribution_amount=25000.0,
            frequency="monthly",
            max_members=5,
            current_round=2,
            status="active"
        )
        db.add(circle)
        db.flush()

        m1 = LendingCircleMember(circle_id=circle.id, user_id=biz_user.id, contribution_status="paid", trust_score=100)
        m2 = LendingCircleMember(circle_id=circle.id, user_id=investor.id, contribution_status="paid", trust_score=95)
        db.add_all([m1, m2])

        print("Seeding audit logs...")
        audit = AuditLog(
            action="SYSTEM_INIT_SEED",
            user_email="admin@demo.com",
            user_id=admin.id,
            category="Security",
            status="success",
            metadata_payload='{"source": "FastAPI Seeder"}'
        )
        db.add(audit)

        db.commit()
        print("[+] Database successfully seeded with demo accounts!")
        print("    Business: business@demo.com / demo1234")
        print("    Investor: investor@demo.com / demo1234")
        print("    Admin:    admin@demo.com / demo1234")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
