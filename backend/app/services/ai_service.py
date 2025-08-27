import os
import requests
from typing import Optional, Dict, Any

class AIService:
    def __init__(self):
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.google_key = os.getenv('GOOGLE_API_KEY')
        
    def get_response(self, prompt: str, system_prompt: str) -> Optional[str]:
        """Get response from available AI service"""
        
        # Try Claude API first
        if self.anthropic_key:
            response = self._call_claude(prompt, system_prompt)
            if response:
                return response
        
        # Try OpenAI
        if self.openai_key:
            response = self._call_openai(prompt, system_prompt)
            if response:
                return response
        
        # Try Google Gemini
        if self.google_key:
            response = self._call_gemini(prompt, system_prompt)
            if response:
                return response
        
        # Fallback response if no AI service is available
        return self._get_fallback_response()
    
    def _call_claude(self, prompt: str, system_prompt: str) -> Optional[str]:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Claude API error: {e}")
            return None
    
    def _call_openai(self, prompt: str, system_prompt: str) -> Optional[str]:
        try:
            import openai
            client = openai.OpenAI(api_key=self.openai_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    
    def _call_gemini(self, prompt: str, system_prompt: str) -> Optional[str]:
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.google_key)
            
            model = genai.GenerativeModel('gemini-pro')
            full_prompt = f"{system_prompt}\n\n{prompt}"
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return None
    
    def _get_fallback_response(self) -> str:
        return """
        Xin lỗi, hệ thống đang gặp sự cố kỹ thuật. 
        
        Trong lúc chờ đợi, bạn có thể thử:
        - Hít thở sâu: Hít vào 4 giây, giữ 4 giây, thở ra 4 giây
        - Đi dạo nhẹ 5-10 phút
        - Nghe nhạc thư giãn
        
        Vui lòng thử lại sau ít phút.
        """