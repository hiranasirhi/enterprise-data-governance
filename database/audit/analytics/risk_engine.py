def calculate_stats(logs):

    total_logs = len(logs)

    failed_logins = len(
        [log for log in logs if "Failed" in log["action"]]
    )

    return {

        "total_logs": total_logs,
        "failed_logins": failed_logins

    }
