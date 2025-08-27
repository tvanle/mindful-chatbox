# Mindful Chatbox - Mental Health Consultation Platform

A Vietnamese web-based chatbot for basic mental health consultation, focusing on stress management and sleep improvement.

## ⚠️ Important Disclaimer

This is a support tool providing basic mental health guidance only. It does NOT replace professional medical consultation. If you're experiencing a crisis, please contact:
- National Mental Health Hotline: **1900-9099**
- Or visit your nearest medical facility immediately

## Features

- 🤖 AI-powered chat using external APIs (Claude/GPT/Gemini)
- 🧘 Stress management advice
- 😴 Sleep improvement tips
- 🚨 Crisis detection and appropriate response
- 💬 Conversation history
- 🌓 Dark/Light theme
- 📱 Responsive design
- 🔒 Privacy-focused (minimal data storage)

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML/CSS/JavaScript (Vanilla)
- **Database**: SQLite (default) / PostgreSQL
- **AI**: External APIs (Claude, OpenAI, Google Gemini)

## Quick Start

### Prerequisites

- Python 3.8+
- API key from at least one provider:
  - [Claude API](https://www.anthropic.com/api)
  - [OpenAI API](https://platform.openai.com/)
  - [Google Gemini](https://makersuite.google.com/app/apikey)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mindful-chatbox.git
cd mindful-chatbox
```

2. Set up backend:
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Run the application:
```bash
python run.py
```

5. Open browser and navigate to:
```
http://localhost:5000
```

The frontend is served directly from Flask's static folder.

## Configuration

Edit `.env` file in the backend folder:

```env
# Choose one or more AI providers
ANTHROPIC_API_KEY=your-claude-api-key
OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-gemini-api-key

# Database (SQLite by default)
DATABASE_URL=sqlite:///mindful_chat.db

# Flask settings
SECRET_KEY=change-this-in-production
FLASK_DEBUG=False

# Crisis hotline
CRISIS_HOTLINE=1900-9099
```

## Project Structure

```
mindful-chatbox/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Prompts & keywords
│   │   ├── services/     # Business logic
│   │   └── database/     # Models
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── config.js
│       ├── chat.js
│       └── ui.js
└── README.md
```

## API Endpoints

- `POST /api/chat` - Send message and get response
- `GET /api/chat/history` - Get conversation history
- `POST /api/feedback` - Submit feedback
- `GET /api/health` - Health check

## Safety Features

- Crisis keyword detection
- Automatic crisis response with hotline information
- Input validation and sanitization
- Rate limiting (20 requests/minute)
- Session-based user tracking (no personal data)

## Development

### Running tests:
```bash
cd backend
pytest tests/
```

### Code formatting:
```bash
black backend/
flake8 backend/
```

### Adding new intents:

Edit `backend/app/core/prompts.py`:
```python
NEW_INTENT_KEYWORDS = ["keyword1", "keyword2"]
```

### Customizing responses:

Modify prompt templates in `backend/app/core/prompts.py`

## Deployment

### Using Docker:

```bash
docker build -t mindful-chatbox .
docker run -p 5000:5000 --env-file .env mindful-chatbox
```

### Production checklist:

- [ ] Set `FLASK_DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Configure proper CORS origins
- [ ] Set up monitoring (Sentry/LogRocket)
- [ ] Implement backup strategy
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up rate limiting with Redis

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/mindful-chatbox/issues)
- Email: support@example.com

## Acknowledgments

- Mental health content guidelines from WHO
- Vietnamese NLP community
- Open source contributors

---

**Remember**: This tool provides general wellness guidance only. Always consult healthcare professionals for medical advice.