from typing import Dict, Any, Optional
from app.core.prompts import (
    CRISIS_KEYWORDS, STRESS_KEYWORDS, SLEEP_KEYWORDS,
    CRISIS_RESPONSE, SYSTEM_PROMPT, get_intent_prompt
)
from app.services.ai_service import AIService
from app.database.models import User, Conversation, db
from datetime import datetime
import uuid

class ChatService:
    def __init__(self):
        self.ai_service = AIService()
    
    def process_message(self, message: str, session_id: str) -> Dict[str, Any]:
        """Process user message and return response"""
        
        # Get or create user
        user = self._get_or_create_user(session_id)
        
        # Check for crisis keywords
        if self._contains_crisis_keywords(message):
            response = CRISIS_RESPONSE
            intent = "crisis"
            is_crisis = True
        else:
            # Detect intent
            intent = self._detect_intent(message)
            
            # Get conversation history for context
            history = self._get_conversation_history(user.id, limit=3)
            
            # Generate prompt
            prompt = get_intent_prompt(intent, message)
            
            # Add context if available
            if history:
                context = "\n".join([f"User: {h['message']}\nBot: {h['response']}" 
                                    for h in history])
                prompt = f"Lịch sử gần đây:\n{context}\n\n{prompt}"
            
            # Get AI response
            response = self.ai_service.get_response(prompt, SYSTEM_PROMPT)
            is_crisis = False
        
        # Save conversation
        conversation = self._save_conversation(
            user_id=user.id,
            message=message,
            response=response,
            intent=intent,
            is_crisis=is_crisis
        )
        
        return {
            "response": response,
            "intent": intent,
            "conversation_id": conversation.id,
            "is_crisis": is_crisis
        }
    
    def _get_or_create_user(self, session_id: str) -> User:
        """Get existing user or create new one"""
        user = User.query.filter_by(session_id=session_id).first()
        
        if not user:
            user = User(session_id=session_id)
            db.session.add(user)
            db.session.commit()
        else:
            user.last_active = datetime.utcnow()
            db.session.commit()
        
        return user
    
    def _contains_crisis_keywords(self, message: str) -> bool:
        """Check if message contains crisis keywords"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in CRISIS_KEYWORDS)
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        message_lower = message.lower()
        
        stress_score = sum(1 for keyword in STRESS_KEYWORDS if keyword in message_lower)
        sleep_score = sum(1 for keyword in SLEEP_KEYWORDS if keyword in message_lower)
        
        if stress_score > sleep_score and stress_score > 0:
            return "stress"
        elif sleep_score > 0:
            return "sleep"
        else:
            return "general"
    
    def _get_conversation_history(self, user_id: str, limit: int = 3) -> list:
        """Get recent conversation history"""
        conversations = Conversation.query.filter_by(
            user_id=user_id,
            is_crisis=False
        ).order_by(
            Conversation.created_at.desc()
        ).limit(limit).all()
        
        return [
            {"message": c.message, "response": c.response}
            for c in reversed(conversations)
        ]
    
    def _save_conversation(self, user_id: str, message: str, response: str, 
                          intent: str, is_crisis: bool) -> Conversation:
        """Save conversation to database"""
        conversation = Conversation(
            user_id=user_id,
            message=message,
            response=response,
            intent=intent,
            is_crisis=is_crisis
        )
        db.session.add(conversation)
        db.session.commit()
        
        return conversation
    
    def get_user_history(self, session_id: str, limit: int = 20) -> list:
        """Get user's conversation history"""
        user = User.query.filter_by(session_id=session_id).first()
        
        if not user:
            return []
        
        conversations = Conversation.query.filter_by(
            user_id=user.id
        ).order_by(
            Conversation.created_at.desc()
        ).limit(limit).all()
        
        return [
            {
                "id": c.id,
                "message": c.message,
                "response": c.response,
                "intent": c.intent,
                "is_crisis": c.is_crisis,
                "created_at": c.created_at.isoformat()
            }
            for c in conversations
        ]