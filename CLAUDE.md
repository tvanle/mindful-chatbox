# Mindful Chatbox - Mental Health Consultation Web Platform

## Project Overview
Web-based Vietnamese chatbox system for basic mental health consultation, specializing in stress management and sleep improvement advice. 

**IMPORTANT**: This system provides general wellness guidance only - NOT medical diagnosis or treatment.

## Technology Stack (Flexible - Choose What Works Best)

### Backend Options
- **Framework**: FastAPI / Flask / Django (tùy chọn)
- **NLP Libraries**: Any Vietnamese NLP library (pyvi, underthesea, vncorenlp, etc.)
- **Database**: Any SQL/NoSQL database you prefer
- **ML Framework**: Use any (TensorFlow, PyTorch, scikit-learn, etc.)

### Frontend Options  
- **Framework**: React / Vue / Angular / Svelte (tự do lựa chọn)
- **UI Library**: Any UI framework (Bootstrap, Tailwind, MUI, Ant Design, etc.)
- **State Management**: Choose what fits (Redux, Zustand, Context API, Pinia, etc.)
- **HTTP Client**: Fetch API, Axios, or any preferred library

### Machine Learning Approach
- **Algorithms**: External APIs or services (GPT, Claude API, Gemini, etc.)
- **Training Data**: Tự thu thập và xây dựng dataset riêng
- **No restrictions on ML libraries or approaches**

## Project Structure

```
mindful-chatbox/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── api/
│   │   │   ├── endpoints/       # API routes
│   │   │   └── websocket.py     # WebSocket handler
│   │   ├── core/
│   │   │   ├── config.py        # Configuration
│   │   │   └── security.py      # Security utils
│   │   ├── models/
│   │   │   ├── nlp_model.py     # NLP processing
│   │   │   └── classifier.py    # Intent classifier
│   │   ├── services/
│   │   │   ├── chat_engine.py   # Chat logic
│   │   │   └── response_gen.py  # Response generation
│   │   └── database/
│   │       ├── models.py        # SQLAlchemy models
│   │       └── redis_cache.py   # Cache layer
│   ├── ml_models/
│   │   ├── intent_classifier/   # Trained models
│   │   └── phobert_fine_tuned/  # Vietnamese BERT
│   ├── data/
│   │   ├── training_data.json   # Training samples
│   │   └── responses.json       # Response templates
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBox/         # Main chat interface
│   │   │   ├── MessageList/     # Message display
│   │   │   └── InputArea/       # User input
│   │   ├── services/
│   │   │   └── api.ts           # API services
│   │   ├── store/               # Redux store
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
│
├── docker-compose.yml
├── nginx.conf
└── README.md
```

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
- Setup FastAPI backend structure
- Create React frontend skeleton
- Implement basic chat UI
- Setup PostgreSQL database

### Phase 2: NLP Integration (Week 3-4)
- Integrate Underthesea for Vietnamese text processing
- Implement intent classification with simple keywords
- Create response template system
- Build training data collection interface

### Phase 3: Machine Learning (Week 5-6)
- Fine-tune PhoBERT for mental health domain
- Train intent classifier
- Implement context-aware responses
- Add sentiment analysis

### Phase 4: Enhancement (Week 7-8)
- Add WebSocket for real-time chat
- Implement session management
- Add typing indicators
- Create admin dashboard

## Core Features

### Chat Engine Components
1. **Input Processing**
   - Vietnamese text normalization
   - Spell checking
   - Intent extraction

2. **Response Generation**
   - Template-based responses
   - Context-aware suggestions
   - Empathetic language patterns

3. **Safety Features**
   - Crisis keyword detection
   - Professional referral system
   - Response validation

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    session_id VARCHAR(255),
    created_at TIMESTAMP,
    last_active TIMESTAMP
);

-- Conversations table  
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    message TEXT,
    response TEXT,
    intent VARCHAR(100),
    sentiment FLOAT,
    created_at TIMESTAMP
);

-- Feedback table
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    conversation_id INT REFERENCES conversations(id),
    helpful BOOLEAN,
    comment TEXT
);
```

## API Endpoints

```python
# Main endpoints
POST   /api/chat/message     # Send message
GET    /api/chat/history     # Get chat history
POST   /api/feedback         # Submit feedback
WS     /ws/chat             # WebSocket connection

# Admin endpoints
GET    /api/admin/analytics  # Usage statistics
POST   /api/admin/responses  # Update responses
GET    /api/admin/logs      # View conversations
```

## Training Data Collection Strategy

### Tự Thu Thập Data
- **Phương pháp**: Tự xây dựng dataset từ đầu
- **Nguồn**: 
  - Survey người dùng thực tế
  - Thu thập câu hỏi thường gặp về sức khỏe tâm thần
  - Tham khảo tài liệu y khoa (chỉ lấy ý tưởng, không copy)
  - Crowdsourcing từ cộng đồng

### Data Structure Example
```json
{
  "training_samples": [
    {
      "user_input": "Tôi cảm thấy căng thẳng quá",
      "intent": "stress",
      "response_type": "breathing_technique",
      "context": "work_stress"
    },
    {
      "user_input": "Không ngủ được mấy ngày rồi",
      "intent": "insomnia",
      "response_type": "sleep_tips",
      "severity": "moderate"
    }
  ]
}
```

### External API Integration
```python
# Example: Using Claude API, GPT, or Gemini
import anthropic  # or openai, google.generativeai

def get_ai_response(user_message):
    # Call external AI service
    # Process and return response
    pass
```

## Development Commands

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev

# Docker deployment
docker-compose up -d

# Run tests
pytest backend/tests/
npm test --prefix frontend

# Lint & Format
black backend/
flake8 backend/
npm run lint --prefix frontend
```

## Sample Code Implementation (Examples - Use Any Framework)

### Backend Example - Flask/FastAPI/Django
```python
# Example with Flask
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    # Call external AI API (Claude, GPT, Gemini, etc.)
    response = process_with_ai(user_message)
    return jsonify({'response': response})

# Or use FastAPI, Django REST, or any framework
```

### Frontend Example - Any Framework
```javascript
// Vanilla JS example
async function sendMessage(message) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message})
    });
    return response.json();
}

// Or use React, Vue, Angular, Svelte - whatever you prefer
```

### AI Integration Examples
```python
# Option 1: Claude API
from anthropic import Anthropic
client = Anthropic(api_key="your-key")
response = client.messages.create(...)

# Option 2: OpenAI GPT
import openai
response = openai.ChatCompletion.create(...)

# Option 3: Google Gemini
import google.generativeai as genai
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(...)

# Option 4: Local model with Transformers
from transformers import pipeline
chatbot = pipeline("text-generation")
response = chatbot(user_input)
```

## Environment Variables

```env
# .env file
DATABASE_URL=postgresql://user:pass@localhost/mindful_chat
REDIS_URL=redis://localhost:6379
MODEL_PATH=./ml_models/phobert_fine_tuned
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000"]
```

## Response Templates

```json
{
  "stress_relief": {
    "breathing_exercise": "Hãy thử kỹ thuật thở 4-7-8: Hít vào 4 giây, giữ 7 giây, thở ra 8 giây...",
    "mindfulness": "Dành 5 phút để tập trung vào hơi thở và cảm nhận hiện tại...",
    "physical_activity": "Đi bộ nhẹ 10-15 phút có thể giúp giảm căng thẳng..."
  },
  "sleep_improvement": {
    "routine": "Thiết lập giờ ngủ cố định, tránh màn hình 1 giờ trước khi ngủ...",
    "environment": "Phòng ngủ nên tối, yên tĩnh và mát mẻ (18-22°C)...",
    "relaxation": "Thử nghe nhạc nhẹ hoặc âm thanh tự nhiên trước khi ngủ..."
  }
}
```

## Safety & Ethics

### Crisis Detection Keywords
```python
CRISIS_KEYWORDS = [
    "tự tử", "muốn chết", "không muốn sống",
    "tự làm hại", "đau khổ quá"
]

CRISIS_RESPONSE = """
Tôi nhận thấy bạn đang trải qua thời gian khó khăn. 
Xin vui lòng liên hệ ngay:
- Tổng đài tư vấn tâm lý: 1900-xxxx
- Bác sĩ chuyên khoa tâm thần
Bạn không đơn độc, luôn có người sẵn sàng giúp đỡ.
"""
```

### Data Privacy
- No personal health information stored
- Sessions expire after 24 hours
- Anonymous usage analytics only
- GDPR/PDPA compliant

## Monitoring & Analytics

```python
# Track metrics
- Response time
- User satisfaction (feedback)
- Most common intents
- Session duration
- Error rates
```

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] ML models loaded
- [ ] SSL certificates installed
- [ ] CORS settings verified
- [ ] Rate limiting enabled
- [ ] Logging configured
- [ ] Backup strategy implemented
- [ ] Monitoring alerts setup
- [ ] Load testing completed