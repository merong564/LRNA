import base64
from openai import OpenAI
from utils.config import OPENAI_API_KEY
from utils.file_handler import encode_image_to_base64

client = OpenAI(api_key=OPENAI_API_KEY)

def get_image_description(image_path, prompt):
    '''
    파일읽기, base64 인코딩, API 호출 예외처리
    '''
    try:
        base64_image = encode_image_to_base64(image_path)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"api 호출 오류 : {str(e)}"
