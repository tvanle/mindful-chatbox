# Mindful Chatbox - Mental Health Consultation Web Platform

## Project Overview
Web-based Vietnamese mental health consultation chatbox using **EXTERNAL AI APIs ONLY** (Claude, GPT, Gemini, etc.)
- Không train model riêng, chỉ dùng AI có sẵn
- Tự chuẩn bị data mẫu, prompt templates, và response patterns
- Focus: Stress management & sleep improvement

## Complete Web Application Requirements

### 1. Core Features (Tính năng chính)
- **Chat Interface**: Giao diện chat real-time
- **User Session Management**: Quản lý phiên chat của user
- **Conversation History**: Lưu và xem lại lịch sử chat
- **Response Feedback**: Đánh giá câu trả lời (helpful/not helpful)
- **Multi-language Support**: Tiếng Việt + English

### 2. User Experience (UX/UI)
- **Responsive Design**: Hoạt động tốt trên mobile/tablet/desktop
- **Typing Indicators**: Hiển thị "bot đang gõ..."
- **Message Status**: Sent/Delivered/Read indicators
- **Dark/Light Mode**: Chế độ sáng/tối
- **Accessibility**: Support screen readers, keyboard navigation
- **Loading States**: Skeleton screens, spinners
- **Error Handling**: User-friendly error messages

### 3. Security & Privacy
- **Data Encryption**: HTTPS, encrypt sensitive data
- **Rate Limiting**: Prevent API abuse
- **Input Validation**: Sanitize user inputs
- **Session Security**: Secure session tokens
- **CORS Configuration**: Proper cross-origin setup
- **API Key Protection**: Environment variables, never expose keys

### 4. Performance Optimization
- **Caching**: Cache common responses
- **Lazy Loading**: Load components on demand
- **Image Optimization**: Compress images, use WebP
- **Code Splitting**: Split bundle for faster loads
- **CDN Integration**: Static assets on CDN
- **Database Indexing**: Optimize queries

### 5. Admin Features
- **Dashboard**: Analytics, user statistics
- **Content Management**: Update prompts, responses
- **User Management**: View/manage user sessions
- **Monitoring**: Track API usage, costs
- **Export Data**: Download chat logs, analytics

### 6. External AI Setup
```javascript
// Prepare data templates for AI
const PROMPT_TEMPLATES = {
  stress: "Bạn là chuyên gia tư vấn sức khỏe tâm thần. User nói: {message}. Hãy tư vấn về quản lý stress...",
  sleep: "Với tư cách consultant về giấc ngủ, hãy tư vấn cho user: {message}..."
}

// Response processing
function processAIResponse(rawResponse) {
  // Format, validate, add safety checks
  return formattedResponse;
}
```

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

## Data Preparation (Chuẩn bị dữ liệu mẫu)

### Prompt Engineering Templates
```json
{
  "system_prompts": {
    "role": "Bạn là chuyên gia tư vấn sức khỏe tâm thần, chuyên về stress và giấc ngủ. Trả lời bằng tiếng Việt, ngắn gọn, thân thiện.",
    "guidelines": [
      "Không đưa ra chẩn đoán y khoa",
      "Luôn khuyên gặp bác sĩ nếu nghiêm trọng",
      "Tập trung vào lời khuyên thực tế"
    ]
  },
  
  "intent_detection": {
    "stress_keywords": ["căng thẳng", "áp lực", "stress", "lo lắng", "bức bối"],
    "sleep_keywords": ["mất ngủ", "khó ngủ", "ngủ không ngon", "thức giấc"],
    "crisis_keywords": ["tự tử", "muốn chết", "không muốn sống"]
  },
  
  "response_templates": {
    "greeting": "Xin chào! Tôi có thể hỗ trợ bạn về vấn đề stress và giấc ngủ. Bạn đang gặp khó khăn gì?",
    "crisis": "Tôi nhận thấy bạn đang rất khó khăn. Vui lòng liên hệ ngay: Tổng đài tâm lý 1900-xxx",
    "unclear": "Bạn có thể chia sẻ rõ hơn về tình trạng của mình được không?"
  }
}
```

### Sample Conversations for Testing
```json
{
  "test_conversations": [
    {
      "user": "Tôi không ngủ được 3 ngày rồi",
      "expected_intent": "insomnia",
      "expected_response_contains": ["thói quen ngủ", "tránh caffeine", "thư giãn"]
    },
    {
      "user": "Công việc làm tôi căng thẳng",
      "expected_intent": "work_stress",
      "expected_response_contains": ["hít thở sâu", "nghỉ ngơi", "ưu tiên công việc"]
    }
  ]
}
```

### API Integration with Safety Layer
```python
def get_safe_ai_response(user_message, conversation_history):
    # 1. Check for crisis keywords first
    if contains_crisis_keywords(user_message):
        return CRISIS_RESPONSE
    
    # 2. Detect intent
    intent = detect_intent(user_message)
    
    # 3. Build context-aware prompt
    prompt = build_prompt(intent, user_message, conversation_history)
    
    # 4. Call external AI
    ai_response = call_ai_api(prompt)  # Claude/GPT/Gemini
    
    # 5. Validate & sanitize response
    safe_response = validate_response(ai_response)
    
    return safe_response
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

## Additional Web App Components

### 7. DevOps & Deployment
- **Version Control**: Git with proper branching strategy
- **CI/CD Pipeline**: Automated testing and deployment
- **Environment Management**: Dev/Staging/Production
- **SSL Certificate**: HTTPS required for production
- **Domain & DNS**: Custom domain setup
- **Backup Strategy**: Regular database backups
- **Monitoring**: Uptime monitoring, error tracking (Sentry)

### 8. Analytics & Tracking
- **User Analytics**: Google Analytics or similar
- **Chat Analytics**: Track popular topics, response quality
- **Performance Metrics**: Page load times, API response times
- **Cost Tracking**: Monitor AI API usage costs
- **A/B Testing**: Test different prompts/UI elements

### 9. Legal & Compliance
- **Terms of Service**: Clear usage terms
- **Privacy Policy**: Data handling disclosure
- **Cookie Consent**: GDPR compliance if needed
- **Disclaimer**: Medical disclaimer prominently displayed
- **Age Verification**: Ensure users are 13+ (or local requirement)

### 10. Testing Strategy
```javascript
// Unit Tests
test('detects stress keywords correctly', () => {
  expect(detectIntent('tôi rất căng thẳng')).toBe('stress');
});

// Integration Tests
test('API returns valid response', async () => {
  const response = await callChatAPI('xin chào');
  expect(response).toHaveProperty('message');
});

// E2E Tests
test('user can send message and receive response', () => {
  // Selenium/Playwright test
});
```

## Deployment Checklist

### Pre-Launch
- [ ] API keys secured in environment variables
- [ ] Database configured and tested
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Error logging setup (console/file/service)
- [ ] Crisis detection tested thoroughly
- [ ] Response time < 3 seconds
- [ ] Mobile responsive tested
- [ ] Cross-browser compatibility checked
- [ ] Load testing completed (handle 100+ concurrent users)

### Security
- [ ] HTTPS enabled
- [ ] Input sanitization implemented
- [ ] XSS protection enabled
- [ ] SQL injection prevention (if using SQL)
- [ ] API authentication implemented
- [ ] Session management secure
- [ ] Sensitive data encrypted

### Production
- [ ] Domain DNS configured
- [ ] SSL certificate installed
- [ ] Monitoring alerts configured
- [ ] Backup automation setup
- [ ] Analytics tracking enabled
- [ ] Error tracking (Sentry) configured
- [ ] Performance monitoring active
- [ ] Documentation completed

### Post-Launch
- [ ] User feedback collection active
- [ ] A/B testing configured
- [ ] Cost monitoring dashboard
- [ ] Regular security audits scheduled
- [ ] Update deployment process documented