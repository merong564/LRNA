from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QTextEdit, QVBoxLayout,QMessageBox,
    QWidget, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import sqlite3

from vision.yolo_detector import YoloV12Detector
from core.prompt_builder import build_prompt
from core.response_parser import parse_gpt_response
from core.db_handler import init_db, insert_record
from api.openai_api import get_image_description
from utils.file_handler import get_image_file

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LRNA - Local Road Navigation Assistant")
        self.setGeometry(100, 100, 900, 600)
        self.image_path = None

        self.init_ui()
        init_db()              # DB 초기화

    def init_ui(self):
        # 이미지 출력 라벨
        self.image_label = QLabel("도로 이미지를 불러오세요")
        self.image_label.setFixedSize(400, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")

        # 이미지 불러오기 버튼
        self.load_button = QPushButton("이미지 열기")
        self.load_button.clicked.connect(self.load_image)

        # 이미지 분석 및 설명 생성 버튼
        self.analyze_button = QPushButton("도로 상태 분석 및 전략 생성")
        self.analyze_button.clicked.connect(self.analyze_image)

        # 텍스트 입력
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("GPT에게 보낼 추가 프롬프트 입력")
        
        # GPT 설명 출력
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        # 레이아웃 설정
        # 상단 수평 레이아웃: 이미지 라벨+이미지 불러오기 버튼
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.image_label)
        top_layout.addWidget(self.load_button)

        # 전체 수직 레이아웃 구성
        layout = QVBoxLayout()

        layout.addLayout(top_layout)                    # 이미지 라벨과 버튼이 나란히 들어간 수평 레이아웃
        layout.addWidget(self.text_input)               # 사용자 입력창 (GPT에게 보낼 프롬프트)
        layout.addWidget(self.analyze_button)           # 이미지 분석 버튼
        layout.addWidget(self.result_output)            # GPT의 결과 텍스트 출력창

        # 레이아웃을 QWidget에 붙이고, 해당 위젯을 윈도우의 중앙 위젯으로 설정
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # 이미지 불러오기 + 이미지 고정
    def load_image(self):
        try:
            path = get_image_file()
            if path:
                pixmap = QPixmap(path).scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
                if pixmap.isNull():
                    raise ValueError("이미지를 불러올 수 없습니다.")
                self.image_label.setPixmap(pixmap)
                self.image_path = path
        except Exception as e:
            QMessageBox.warning(self, "오류", f"이미지 불러오기 실패: {e}")

    # 전체 실행
    def analyze_image(self):
            if not self.image_path:
                QMessageBox.warning(self, "알림", "먼저 이미지를 불러와 주세요.")
                return

            try:
                # 1. Vision 분석
                detections = self.process_image(self.image_path)
                user_prompt = self.text_input.toPlainText()        # 사용자의 지시문을 문자열로 받아 GPT 프롬프트에 덧붙이기
                # 2. GPT 프롬프트 생성 및 호출
                strategy_data = self.generate_strategy(detections, user_prompt)
                # 3. DB 저장
                self.save_result_to_db(detections, strategy_data)
                # 4. 결과 GUI 표시
                self.display_result(detections, strategy_data)

            except Exception as e:
                QMessageBox.critical(self, "오류", f"분석 중 오류 발생:\n{e}")

    # Vision 분석
    def process_image(self, image_path):
        """
        YOLO detection 수행
        """
        detect = YoloV12Detector()
        yolo_results = detect.detect_objects(image_path)

        return yolo_results
    
    # GPT 프롬프트 생성 및 호출
    def generate_strategy(self, detections, user_prompt=""):
        """
        GPT 프롬프트 생성 → API 호출 → 응답 파싱
        """
        prompt = build_prompt(detections)
        if user_prompt:
            prompt += f"\n\n사용자 추가 요청: {user_prompt}"

        gpt_response = get_image_description(self.image_path, prompt)
        parsed = parse_gpt_response(gpt_response)
        return parsed
    
    # DB 저장
    def save_result_to_db(self, detections, strategy_data):
        insert_record(
            detections,
            strategy_data.get("strategy", "없음"),      # strategy 키가 없을 경우 없음을 저장
            strategy_data.get("reason", "없음")         # reason 키가 없을 경우 없음을 저장
        )

    # 결과 표시
    def display_result(self, detections, strategy_data):
        text = (
            f"[탐지 결과]\n{detections}\n\n"
            f"[전략]\n{strategy_data['strategy']}\n\n"
            f"[근거]\n{strategy_data['reason']}"
        )
        self.result_output.setPlainText(text)