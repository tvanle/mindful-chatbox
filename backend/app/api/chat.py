from flask import Blueprint, request, jsonify, session
from app.services.chat_service import ChatService
from app.database.models import Feedback, Conversation, db
import uuid
import time

chat_bp = Blueprint('chat', __name__)
chat_service = ChatService()

# Rate limiting dictionary (simple implementation)
rate_limit_dict = {}
RATE_LIMIT_PER_MINUTE = 20

@chat_bp.before_request
def check_rate_limit():
    """Simple rate limiting"""
    client_ip = request.remote_addr
    current_minute = int(time.time() / 60)
    
    key = f"{client_ip}:{current_minute}"
    
    if key in rate_limit_dict:
        if rate_limit_dict[key] >= RATE_LIMIT_PER_MINUTE:
            return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
        rate_limit_dict[key] += 1
    else:
        # Clean old entries
        rate_limit_dict.clear()
        rate_limit_dict[key] = 1

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        message = data['message'].strip()
        
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        if len(message) > 1000:
            return jsonify({"error": "Message too long (max 1000 characters)"}), 400
        
        # Get or create session ID
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        session_id = session['session_id']
        
        # Process message
        result = chat_service.process_message(message, session_id)
        
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({
            "error": "An error occurred processing your message"
        }), 500

@chat_bp.route('/chat/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    try:
        if 'session_id' not in session:
            return jsonify({"data": []})
        
        limit = request.args.get('limit', 20, type=int)
        limit = min(limit, 100)  # Max 100 messages
        
        history = chat_service.get_user_history(session['session_id'], limit)
        
        return jsonify({
            "success": True,
            "data": history
        })
        
    except Exception as e:
        print(f"History error: {e}")
        return jsonify({"error": "Failed to fetch history"}), 500

@chat_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback for a conversation"""
    try:
        data = request.get_json()
        
        if not data or 'conversation_id' not in data:
            return jsonify({"error": "Conversation ID is required"}), 400
        
        conversation_id = data['conversation_id']
        helpful = data.get('helpful', None)
        comment = data.get('comment', '')
        
        # Verify conversation exists
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404
        
        # Check if feedback already exists
        existing_feedback = Feedback.query.filter_by(
            conversation_id=conversation_id
        ).first()
        
        if existing_feedback:
            # Update existing feedback
            existing_feedback.helpful = helpful
            existing_feedback.comment = comment
        else:
            # Create new feedback
            feedback = Feedback(
                conversation_id=conversation_id,
                helpful=helpful,
                comment=comment
            )
            db.session.add(feedback)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Thank you for your feedback!"
        })
        
    except Exception as e:
        print(f"Feedback error: {e}")
        return jsonify({"error": "Failed to submit feedback"}), 500

@chat_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Mindful Chatbox API"
    })