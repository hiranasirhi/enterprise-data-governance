from flask import Blueprint, render_template, request, Response, stream_with_context
from flask_login import login_required
from config.database import db
from database.audit.models.user_activity_model import UserActivity
from database.audit.models.audit_model import AuditLog
from database.audit.models.user_model import User
from database.audit.models.resource_model import DataResource
from database.access_workflow.models.access_request import AccessRequest
from groq import Groq
import json
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ai_reports_bp = Blueprint("ai_reports_bp", __name__)

def get_system_data():
    total_users = User.query.count()
    blocked_users = User.query.filter_by(is_blocked=True).count()
    blocked_list = User.query.filter_by(is_blocked=True).all()

    total_activities = UserActivity.query.count()
    flagged = UserActivity.query.filter_by(is_flagged=True).count()
    high_risk = UserActivity.query.filter(UserActivity.risk_score >= 70).count()

    risky = UserActivity.query.filter(
        UserActivity.risk_score >= 70
    ).order_by(UserActivity.timestamp.desc()).limit(10).all()

    risky_list = [
        f"{a.user.full_name if a.user else 'Unknown'} performed {a.action} on "
        f"{a.resource.resource_name if a.resource else 'Unknown'} "
        f"(risk score: {a.risk_score})"
        for a in risky
    ]

    total_requests = AccessRequest.query.count()
    pending = AccessRequest.query.filter_by(status="Pending").count()
    approved = AccessRequest.query.filter_by(status="Approved").count()
    rejected = AccessRequest.query.filter_by(status="Rejected").count()
    revoked = AccessRequest.query.filter_by(status="Revoked").count()

    actions = ["READ", "WRITE", "DELETE", "UPDATE", "EXPORT"]
    action_counts = {
        a: UserActivity.query.filter_by(action=a).count() for a in actions
    }

    total_logs = AuditLog.query.count()
    recent_logs = AuditLog.query.order_by(
        AuditLog.timestamp.desc()
    ).limit(5).all()
    recent_log_list = [
        f"{l.user.full_name if l.user else 'Unknown'} - {l.action} "
        f"(risk: {l.risk_score}) at {l.timestamp}"
        for l in recent_logs
    ]

    user_roles_query = db.session.execute(db.text("""
        SELECT u.full_name, r.role_name, d.dept_name,
               CASE WHEN u.is_blocked THEN 'Blocked' ELSE 'Active' END as status
        FROM Users u
        LEFT JOIN User_Roles ur ON u.user_id = ur.user_id
        LEFT JOIN Roles r ON ur.role_id = r.role_id
        LEFT JOIN Departments d ON u.dept_id = d.dept_id
    """)).fetchall()

    user_roles_list = [
        f"{row[0]} - Role: {row[1] or 'No Role'}, Dept: {row[2] or 'N/A'}, Status: {row[3]}"
        for row in user_roles_query
    ]

    resources = DataResource.query.all()
    resource_list = [
        f"{r.resource_name} (Sensitivity: {r.sensitivity_level})"
        for r in resources
    ]

    return {
        "total_users": total_users,
        "blocked_users": blocked_users,
        "blocked_list": [u.full_name for u in blocked_list],
        "total_activities": total_activities,
        "flagged_activities": flagged,
        "high_risk_activities": high_risk,
        "risky_activities": risky_list,
        "total_requests": total_requests,
        "pending_requests": pending,
        "approved_requests": approved,
        "rejected_requests": rejected,
        "revoked_requests": revoked,
        "action_breakdown": action_counts,
        "total_audit_logs": total_logs,
        "recent_audit_logs": recent_log_list,
        "user_roles": user_roles_list,
        "resources": resource_list,
    }


def build_prompt(report_type, data):
    base_context = f"""
You are a senior enterprise security analyst writing a formal governance report.
Here is the current live system data:

USERS: {data['total_users']} total, {data['blocked_users']} blocked
Blocked users: {', '.join(data['blocked_list']) if data['blocked_list'] else 'None'}

ACTIVITY: {data['total_activities']} total activities, {data['flagged_activities']} flagged, {data['high_risk_activities']} high risk
Action breakdown: {json.dumps(data['action_breakdown'])}

High risk activities:
{chr(10).join(data['risky_activities']) if data['risky_activities'] else 'None'}

ACCESS REQUESTS: {data['total_requests']} total
- Pending: {data['pending_requests']}
- Approved: {data['approved_requests']}
- Rejected: {data['rejected_requests']}
- Revoked: {data['revoked_requests']}

AUDIT LOGS: {data['total_audit_logs']} total
Recent logs:
{chr(10).join(data['recent_audit_logs'])}

USER ROLES:
{chr(10).join(data['user_roles'])}

DATA RESOURCES:
{chr(10).join(data['resources'])}
"""

    prompts = {
        "security": base_context + """
Generate a professional SECURITY SUMMARY REPORT with these sections:
1. Executive Summary
2. Current Security Posture (rate it: Critical/High/Medium/Low risk)
3. Key Threats Identified
4. High Risk Activities Analysis
5. Blocked Users Analysis
6. Immediate Recommendations (numbered list)
7. Long Term Recommendations

Use clear headings, be specific with numbers from the data, and write in formal enterprise language.
""",
        "behavior": base_context + """
Generate a professional USER BEHAVIOR ANALYSIS REPORT with these sections:
1. Executive Summary
2. Overall User Activity Overview
3. Suspicious User Profiles (based on high risk scores and flagged activities)
4. Action Pattern Analysis (what actions are most common and concerning)
5. Blocked Users Investigation Summary
6. Behavioral Risk Indicators
7. Recommendations for User Monitoring

Be specific about which users and actions are concerning. Use formal language.
""",
        "access": base_context + """
Generate a professional ACCESS CONTROL REPORT with these sections:
1. Executive Summary
2. Current Access Request Status Overview
3. Role Distribution Analysis
4. Resource Access Patterns
5. Revoked and Rejected Access Analysis
6. Access Control Gaps Identified
7. Recommendations for Access Policy Improvements

Focus on who has access to what and whether it is appropriate. Use formal language.
""",
        "compliance": base_context + """
Generate a professional COMPLIANCE REPORT with these sections:
1. Executive Summary
2. Compliance Posture Overview
3. Policy Violations Detected
4. High Risk Resource Access Analysis
5. Audit Trail Completeness Assessment
6. Data Sensitivity Compliance Check
7. Compliance Gaps and Remediation Steps
8. Overall Compliance Score (out of 100) with justification

Be specific about violations and gaps found in the data. Use formal enterprise language.
"""
    }

    return prompts.get(report_type, prompts["security"])


@ai_reports_bp.route("/")
@login_required
def ai_reports():
    return render_template("ai_reports.html")


@ai_reports_bp.route("/generate/<report_type>", methods=["POST"])
@login_required
def generate_report(report_type):
    data = get_system_data()
    prompt = build_prompt(report_type, data)

    def stream():
        try:
            client = Groq(api_key=GROQ_API_KEY)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                stream=True
            )
            for chunk in completion:
                text = chunk.choices[0].delta.content
                if text:
                    yield f"data: {json.dumps({'text': text})}\n\n"
            yield "data: {\"done\": true}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(stream()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
