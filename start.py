
import uvicorn
import os
import sys
from pathlib import Path


project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    
    print("🍳 Starting Smart Recipe Recommendation API...")
    print("🌐 Visit http://localhost:8000/static/index.html to access the app")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🤖 Add your OpenAI API key to .env for AI recommendations")
    print("-" * 60)
    
    
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found. Please copy .env.example to .env")
        print("   Optional: OPENAI_API_KEY (for AI recommendations)")
        print("-" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
