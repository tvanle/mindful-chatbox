import os

# Crisis keywords for detection
CRISIS_KEYWORDS = [
    "tự tử", "muốn chết", "không muốn sống", "tự làm hại",
    "đau khổ quá", "chết", "kết thúc tất cả", "không còn hy vọng",
    "suicide", "kill myself", "end it all", "no hope"
]

# Intent keywords
STRESS_KEYWORDS = [
    "căng thẳng", "áp lực", "stress", "lo lắng", "bức bối",
    "lo âu", "bồn chồn", "khó chịu", "mệt mỏi", "kiệt sức"
]

SLEEP_KEYWORDS = [
    "mất ngủ", "khó ngủ", "ngủ không ngon", "thức giấc",
    "ngủ", "giấc ngủ", "buồn ngủ", "ngáy", "ác mộng"
]

# Response templates
CRISIS_RESPONSE = f"""
Tôi nhận thấy bạn đang trải qua thời gian rất khó khăn. Xin vui lòng liên hệ ngay với:

📞 Tổng đài tư vấn tâm lý quốc gia: {os.getenv('CRISIS_HOTLINE', '1900-9099')}
🏥 Hoặc đến ngay cơ sở y tế gần nhất

Bạn không đơn độc. Luôn có người sẵn sàng lắng nghe và giúp đỡ bạn.
"""

# System prompts for AI
SYSTEM_PROMPT = """
Bạn là một chuyên gia tư vấn sức khỏe tâm thần thân thiện, chuyên về quản lý stress và cải thiện giấc ngủ.

NGUYÊN TẮC QUAN TRỌNG:
1. KHÔNG đưa ra chẩn đoán y khoa
2. KHÔNG kê đơn thuốc
3. Luôn khuyên gặp bác sĩ nếu tình trạng nghiêm trọng
4. Trả lời bằng tiếng Việt, ngắn gọn (2-3 đoạn)
5. Thân thiện, đồng cảm, và tích cực
6. Tập trung vào lời khuyên thực tế có thể áp dụng ngay

Chuyên môn của bạn:
- Kỹ thuật thở và thư giãn
- Vệ sinh giấc ngủ
- Quản lý stress hàng ngày
- Mindfulness và thiền cơ bản
- Lối sống lành mạnh
"""

def get_intent_prompt(intent, user_message):
    prompts = {
        "stress": f"""
Người dùng đang gặp vấn đề về stress/căng thẳng. Tin nhắn: "{user_message}"

Hãy đưa ra 2-3 lời khuyên cụ thể, thực tế để giảm stress ngay lập tức.
Có thể bao gồm: kỹ thuật thở, thư giãn cơ, hoặc thay đổi góc nhìn.
""",
        
        "sleep": f"""
Người dùng đang gặp vấn đề về giấc ngủ. Tin nhắn: "{user_message}"

Hãy đưa ra 2-3 lời khuyên cải thiện giấc ngủ dựa trên nguyên tắc vệ sinh giấc ngủ.
Có thể bao gồm: thói quen trước ngủ, môi trường ngủ, hoặc kỹ thuật thư giãn.
""",
        
        "general": f"""
Tin nhắn từ người dùng: "{user_message}"

Hãy trả lời một cách hữu ích, tập trung vào sức khỏe tâm thần và cảm xúc.
Nếu không rõ vấn đề, hãy hỏi thêm thông tin một cách tế nhị.
"""
    }
    
    return prompts.get(intent, prompts["general"])