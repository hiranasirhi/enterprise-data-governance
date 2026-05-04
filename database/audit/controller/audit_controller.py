from database.audit.services.audit_services import fetch_audit_logs
from database.audit.analytics.risk_engine import calculate_stats


def get_audit_dashboard_data():

    logs = fetch_audit_logs()

    stats = calculate_stats(logs)

    return {
        "logs": logs,
        "stats": stats
    }
