from database.audit.models.audit_model import AuditLog

def fetch_audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return [
        {
            "user": log.user.full_name if log.user else "Unknown",
            "resource": log.resource.resource_name if log.resource else "Unknown",
            "action": log.action,
            "risk_score": log.risk_score,
            "ip_address": log.ip_address or "N/A",
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M") if log.timestamp else ""
        }
        for log in logs
    ]
