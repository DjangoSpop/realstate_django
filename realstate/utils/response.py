def success_response(data=None, pagination=None):
    return {
        "success": True,
        "data": data,
        "pagination": pagination,
    }

def error_response(code, message, details=None):
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        }
    }
