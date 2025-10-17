"""
GPT 프롬프트 생성 모듈
- Vision 모듈에서 전달받은 객체 인식 결과(detections)를 기반으로
  ChatGPT에게 전달할 프롬프트를 구성합니다.
"""

import json

def build_prompt(detections: list) -> str:
    """
    detections: [
        {"label": "pothole", "confidence": 0.93, "position": "left lane"},
        {"label": "person", "confidence": 0.88, "position": "front right"}
    ]
    """
    ## 파이썬 리스트를 json 문자열로 변환
    # ensure_ascii=False: 영문 아스키코드 사용 시 한글 깨짐, False하여 한글 보이게 하기
    # indent=2: json 문자열 보기 좋게 2칸 들여쓰기
    detections_text = json.dumps(detections, ensure_ascii=False, indent=2)

    prompt = f"""
주어진 도로 이미지와 객체 인식 결과를 기반으로 주행 전략과 근거를 JSON 형식으로 제시하세요.

객체 인식 결과:
{detections_text}

조건:
- 안전을 최우선으로 고려할 것
- strategy(전략)는 구체적인 주행 지시를 자연어로 출력
- reason(근거)는 왜 이런 전략을 세웠는지 간단히 설명
- 반드시 JSON 형식으로 출력할 것

출력 예시:
{{
  "strategy": "왼쪽 차선에 포트홀이 있으므로 중앙 차선으로 이동하세요.",
  "reason": "탐지 결과 왼쪽 차선에서 포트홀이 확인되어 차량 손상을 방지하기 위해 회피가 필요합니다."
}}
"""
    return prompt.strip()