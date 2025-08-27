from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Mindful Chatbox on http://localhost:{port}")
    print("Press CTRL+C to stop the server")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )