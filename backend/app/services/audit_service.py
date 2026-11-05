import json
from typing import Optional, Any
from sqlalchemy.orm import Session
from app.models.models import AuditLog

def log_event(
    db: Session,
    action: str,
    user_email: str,
    category: str = "Financial",
    status: str = "info",
    user_id: Optional[str] = None,
    ip_address: str = "127.0.0.1",
    metadata: Optional[Any] = None
) -> AuditLog:
    meta_str = json.dumps(metadata) if metadata is not None else None
    audit = AuditLog(
        action=action,
        user_email=user_email,
        category=category,
        status=status,
        user_id=user_id,
        ip_address=ip_address,
        metadata_payload=meta_str
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit
