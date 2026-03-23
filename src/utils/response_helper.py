from flask import jsonify

def standard_response(message, result=None, status_code=200):
    return jsonify({
        "message": message,
        "result": result,
        "status": "success" if status_code < 400 else "error"
    }), status_code