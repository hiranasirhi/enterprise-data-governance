def validate_request(data):
    required = ["user_id", "resource_id", "manager_id"]

    for field in required:
        if field not in data:
            return False

    return True
