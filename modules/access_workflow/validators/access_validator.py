def validate_request(data):
    if "user_id" not in data or "resource_id" not in data:
        return False
    return True
