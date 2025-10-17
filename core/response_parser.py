"""
ChatGPT 응답 파싱 모듈
- ChatGPT에서 받은 문자열 응답을 JSON으로 안전하게 변환합니다.
"""

import json

def parse_gpt_response(response_text: str) -> dict:
    """
    ChatGPT의 응답에서 JSON 부분만 추출하여 dict로 변환
    """
    try:
        # JSON 블록만 추출 (응답에 코드블록 표식이 포함된 경우 대비)
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        json_str = response_text[start:end]
        parsed = json.loads(json_str)
        return parsed
    except Exception as e:
        print(f"[ERROR] GPT 응답 파싱 실패: {e}")
        return {"strategy": "분석 실패", "reason": "GPT 응답 포맷이 올바르지 않습니다."}