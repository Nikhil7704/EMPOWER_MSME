import uvicorn
import os
import sys

# Ensure backend root is in PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[*] Starting EmpowerMSME FastAPI Server on http://127.0.0.1:{port}")
    print(f"[*] Interactive Swagger API Docs at http://127.0.0.1:{port}/docs")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
