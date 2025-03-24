import subprocess
import time
import os
import sys
import webbrowser
import threading

def start_ollama():
    print("Starting Ollama...")
    ollama_process = subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return ollama_process

def start_api():
    print("Starting API server...")
    api_process = subprocess.Popen(
        [sys.executable, "api.py"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return api_process

def start_n8n():
    print("Starting n8n...")
    n8n_process = subprocess.Popen(
        ["n8n", "start"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return n8n_process

def start_frontend():
    print("Starting frontend...")
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "second-brain-ui")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return frontend_process

def log_output(process, name):
    for line in process.stdout:
        print(f"[{name}] {line.strip()}")
    for line in process.stderr:
        print(f"[{name} ERROR] {line.strip()}")

def main():
    print("Starting Second Brain system...")
    
    # Start Ollama
    ollama_process = start_ollama()
    threading.Thread(target=log_output, args=(ollama_process, "Ollama"), daemon=True).start()
    
    # Wait for Ollama to start
    time.sleep(5)
    
    # Start API server
    api_process = start_api()
    threading.Thread(target=log_output, args=(api_process, "API"), daemon=True).start()
    
    # Start n8n
    n8n_process = start_n8n()
    threading.Thread(target=log_output, args=(n8n_process, "n8n"), daemon=True).start()
    
    # Start frontend
    frontend_process = start_frontend()
    threading.Thread(target=log_output, args=(frontend_process, "Frontend"), daemon=True).start()
    
    # Wait for services to start
    time.sleep(10)
    
    # Open browser
    print("Opening browser...")
    webbrowser.open("http://localhost:5173") 
    
    print("Second Brain system is running!")
    print("- Frontend: http://localhost:5173") 
    print("- API: http://localhost:5000") 
    print("- n8n: http://localhost:5678") 
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        ollama_process.terminate()
        api_process.terminate()
        n8n_process.terminate()
        frontend_process.terminate()
        print("System stopped.")

if __name__ == "__main__":
    main()
