# server.py
from flask import Flask, request, jsonify
import os
import threading
import time
import json
import logging
import importlib.util
import glob

app = Flask(__name__)

# Dictionary to track ongoing request threads
requests_threads = {}

# Configure logging
logging.basicConfig(filename='RWS_log.txt', level=logging.DEBUG, format='%(asctime)s - %(message)s')

def log_status(message):
    logging.debug(message)
    print(message)  # Debugging output

# Function to dynamically load services
services = {}

def load_services():
    global services
    services.clear()
    service_files = glob.glob("services/*.py")
    for file in service_files:
        module_name = os.path.basename(file)[:-3]
        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "execute"):
            services[module_name] = module.execute
            print(f"[Server] Loaded service: {module_name}")  # Debugging output

def process_request(request_id, service_name, sub_json, request_type):
    try:
        log_status(f"Processing request ID {request_id} for service {service_name}")
        time.sleep(2)

        if service_name in services:
            result = services[service_name](sub_json)
            send_response(request_id, result, request_type)
        else:
            log_status(f"Service {service_name} not found.")
    except Exception as e:
        send_response(request_id, {"error": str(e)}, request_type)

def send_response(request_id, result, request_type):
    try:
        response_json = {"status": "SUCCESS", "error_reason": "NONE", "data": result}
        log_status(f"Response for Request_ID {request_id}: {json.dumps(response_json, indent=4)}")
    except Exception as e:
        log_status(f"Error preparing response: {e}")

@app.route('/web_server', methods=['POST'])
def web_server():
    try:
        data = request.get_json()
        log_status(f"Received JSON: {json.dumps(data, indent=4)}")

        required_keys = ["Request_ID", "Service_Name", "Sub_JSON", "Request_Type"]
        if not all(key in data for key in required_keys):
            return jsonify({"status": "ERROR", "error_reason": "INVALID_ARGUMENT", "data": {}})

        request_id = data["Request_ID"]
        service_name = data["Service_Name"]
        sub_json = data["Sub_JSON"]
        request_type = data["Request_Type"]

        if service_name not in services:
            return jsonify({"status": "ERROR", "error_reason": "SERVICE_NOT_FOUND", "data": {}})

        if request_type == "INLINE":
            result = services[service_name](sub_json)
            return jsonify({"status": "SUCCESS", "error_reason": "NONE", "data": result})

        if request_type == "FUTURE_CALL":
            if request_id not in requests_threads:
                thread = threading.Thread(target=process_request, args=(request_id, service_name, sub_json, request_type))
                requests_threads[request_id] = thread
                thread.start()

            return jsonify({"status": "INPROGRESS", "error_reason": "NONE", "data": {}})

        return jsonify({"status": "ERROR", "error_reason": "INVALID_ARGUMENT", "data": {}})

    except Exception as e:
        log_status(f"Error in web_server function: {e}")
        return jsonify({"status": "ERROR", "error_reason": "SERVICE_ERROR", "data": {}})

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Web Server to process requests")
    parser.add_argument('port_no', type=int, help="Port number to run the server on")
    args = parser.parse_args()

    load_services()
    log_status(f"Starting server on port {args.port_no}")
    app.run(debug=True, host='0.0.0.0', port=args.port_no)
