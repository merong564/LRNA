# LRNA(Local Road Navigation Assistant)

## 📌 주제 및 선정배경

- 기존의 네비게이션은 출발지-목적지 경로 안내에 집중되어 있어 공사구간, 포트홀, 차선 손상과 같은 **local 도로 상황을 반영하지 못한다.**

- 이런 로컬 요소들은 GPS/지도 데이터로는 파악이 어렵고, 실제 주행 시 카메라, LiDAR 등 **센서 기반 인식이 필수적**이다.

- 카메라 이미지로 **도로 상황을 인식**하고 이를 **ChatGPT와 결합하여 주행 전략을 생성**하고, **운전자와 주행 전략에 대해 질의응답**이 가능하도록 한다.



## 🎯 목표

1. **도로 상태 인지**
    
    카메라로 촬영한 도로 이미지에서 YOLOv12, OpenCV를 이용하여 도로 상태를 인식한다.
    
    - **YOLOv12 사용 이유 : 인식 안전성, 실시간성 확보**
        - 자율주행 특성상 실시간 처리, 지연 최소화 필수
        - 객체 위치 정보 수집 가능 → 주행 경로 생성에 활용

    - **OpenCV 사용 이유: 차선 인식**
        - Canny edge detection을 통한 차선 segmentation

    - **도로 상태 예시**
        - 장애물, 사람, 도로 포트홀, 차선 훼손정도, 교통안전표지, 도로노면표지


<br />

2. **주행 전략 제시**
    
    ChatGPT를 활용하여 도로 상황을 해석하고, 이에 따라 주행 전략을 제안한다.
    
    1) 도로 이미지와 인식 결과를 입력
    
    2) 프롬프트 생성
    
    3) OpenAI API로 프롬프트 전달, ChatGPT의 응답을 PyQt GUI에 표시
    
    4) 주행 전략 및 근거를 DB에 기록
    
<br />

3. **휴먼 인터페이스 구축**
    
    운전자가 주행 전략에 대해 질문할 경우, 전략 선정 이유를 답변한다.
    
    1) 사용자가 프롬프트에 질문
    
    2) DB에서 해당 기록을 불러옴
    
    3) GPT가 전략, 근거를 자연어로 답변
    
    ![image.png](https://github.com/user-attachments/assets/f2ec264a-9746-45b4-bb59-7350e8e6c132)
    

## 🧩 사용 기술

- 프로그래밍 언어: Python
- 딥러닝 모델/컴퓨터 비전: YOLOv12, OpenCV
    - 데이터셋: AIHub
- 언어 모델: OpenAI API
- GUI: PyQt5
- DB: SQLite3
- 환경설정: dotenv (.env 환경변수)

## 🔁 전체 흐름

1. 이미지 입력
    - 사용자가 주행 환경 이미지를 업로드

1. 환경 인식
    - YOLOv12/OpenCV로 이미지 기반 객체 인식 수행

1. 전략 생성
    - 인식 결과를 ChatGPT에 전달
    - 주행 전략과 근거 생성

1. 저장 및 제공
    - 전략과 근거를 DB에 저장
    - 운전자에게 전략 안내

1. 휴먼 인터페이스 질의응답
    - 사용자가 질문
    - DB에 저장된 근거를 불러와 ChatGPT가 답변

## 🔧 시스템 구성도 (Architecture)

![image.png](https://github.com/user-attachments/assets/20871cce-4ac1-4818-a4d1-bf40fe84c102)

## 📁 디렉토리 구조

```
LRNA/
├── gui/                          
│   └── main_app.py               	# PyQt5 GUI 실행
│
├── vision/                       
│   ├── yolo_detector.py          	# YOLOv12 탐지 모듈
│   └── lane_detection.py         	# OpenCV 차선 인식 모듈
│
├── api/                          
│   └── openai_api.py             	# OpenAI API 호출 모듈
│
├── core/
│   ├── prompt_builder.py         # GPT 프롬프트 생성
│   ├── response_parser.py      # GPT JSON 응답 파싱 
│   └── db_handler.py             	# DB 저장/조회 함수 
│
├── db/                           
│   └── driving_log.db            	# SQLite DB
│
├── utils/                        
│   └── file_handler.py           	# 파일/이미지 처리
│
├── main.py                       	# 메인 실행 파일
├── .env                          	# 환경 변수 
└── requirements.txt              	# 패키지 목록
```

## 📷 예시 시나리오

**도로 공사로 인해 차선을 변경할 경우**

- 자율주행차의 카메라가 도로 환경을 촬영

- 공사 표지판과 차선 축소 구간을 인식

- ChatGPT의 주행 전략 생성
<br />
    “안전을 위해 좌측 차선으로 변경하세요.”

- 운전자가 주행 전략에 대해 질문
<br />
    “왜 차선을 변경하나요?”

- ChatGPT의 답변 출력
<br />
    “전방에 공사 진행 중으로, 우측 차선이 폐쇄되었기 때문에 좌측 차선으로 안내했습니다.”

<br />

**외에도 다양한 시나리오 존재**

- 좌회전 노면표시 인식 후 좌회전 차선으로 이동

- 포트홀 회피

- 보행자/동물 돌발 출현 시 정지

## 🚀 확장 아이디어

- **센서 연결**
    - LiDAR, radar 등의 거리 센서 사용
    → 객체의 정확한 위치 정보 활용
    - 실제 카메라 사용
    → 실시간 영상처리 진행
- **경로 생성 알고리즘 사용**
    - 실시간 경로 생성 알고리즘과 연계하여 회피 주행 경로를 동적으로 생성
    - DWA(Dynamic Window Approach), TEB(Time Elastic Band) 등
- **음성 피드백**
    - 실제 네비게이션처럼 음성 안내 제공
    - ChatGPT가 생성한 주행 전략을 TTS(Text-to-Speech) 엔진으로 변환

## 자료

1. **데이터셋**
    - 수도권 지역 도로상의 장애물 및 도로 표면의 이상 상태 인지를 위한 영상 및 이미지 데이터
        
        [도로장애물/표면 인지 영상(수도권)](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=179)
        
        [고해상도 도로노면 이미지 데이터](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=71781)
        
        ![image.png](https://github.com/user-attachments/assets/1c2affd8-fc62-49c0-a656-23ce5700be4f)
        

2. **Yolov12 pretrained model**
<br />
    - [github link](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/models/12/yolo12.yaml)