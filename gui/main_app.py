from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QTextEdit, QVBoxLayout,QMessageBox,
    QWidget, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from api.openai_api import get_image_description
from utils.file_handler import get_image_file, encode_image_to_base64
from utils.config import DB_PATH
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenAI 이미지 설명 프로그램")
        self.setGeometry(100, 100, 700, 500)
        self.image_path = None
        self.init_ui()
        self.init_db()

    def init_ui(self):
        # 이미지 출력 라벨
        self.image_label = QLabel("이미지를 불러오세요")
        self.image_label.setFixedSize(300, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")

        # 이미지 불러오기 버튼
        self.load_button = QPushButton("이미지 열기")
        self.load_button.clicked.connect(self.load_image)

        # 텍스트 입력
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("GPT에게 보낼 추가 프롬프트 입력")
        
        # GPT 설명 출력
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        # 설명 생성 버튼
        self.generate_button = QPushButton("GPT 설명 생성")
        self.generate_button.clicked.connect(self.generate_description)

        # 레이아웃 설정
        # 상단 수평 레이아웃: 이미지 라벨+이미지 불러오기 버튼
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.image_label)
        top_layout.addWidget(self.load_button)

        # 전체 수직 레이아웃 구성
        layout = QVBoxLayout()

        # 첫 번째 줄: 이미지 라벨과 버튼이 나란히 들어간 수평 레이아웃
        layout.addLayout(top_layout)
        # 두 번째 줄: 사용자 입력창 (GPT에게 보낼 프롬프트)
        layout.addWidget(self.text_input)
        # 세 번째 줄: GPT 설명 생성 버튼
        layout.addWidget(self.generate_button)
        # 네 번째 줄: GPT의 결과 텍스트 출력창
        layout.addWidget(self.result_output)

        # 레이아웃을 QWidget에 붙이고, 해당 위젯을 윈도우의 중앙 위젯으로 설정
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()          # 커서 생성
        # 커리 생성
        cursor.execute('''               
            CREATE TABLE IF NOT EXISTS image_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image BLOB,
                prompt TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

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

    # GPT 설명 생성
    def generate_description(self):
        if not self.image_path:
            self.result_output.setPlainText("이미지를 먼저 불러와 주세요.")
            return
        
        prompt = self.text_input.toPlainText()
        result = get_image_description(self.image_path, prompt)
        self.result_output.setPlainText(result)

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            with open(self.image_path, "rb") as f:
                image_blob = f.read()
            cursor.execute('''
                INSERT INTO image_logs (image, prompt, response) VALUES (?, ?, ?)
            ''', (image_blob, prompt, result))
            conn.commit()

