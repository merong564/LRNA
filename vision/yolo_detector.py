from ultralytics import YOLO
import os

class YoloV12Detector:
    def __init__(self, model_name="yolo12n.pt"):
        """
        YOLOv12 pretrained model 로드
        model_name: 가장 작고 빠른 모델인 yolo12n.pt를 디폴트로 사용
        """

        try:
            if not os.path.exists(model_name):
                print(f"[INFO] '{model_name}' 파일이 로컬에 없습니다. Ultralytics에서 자동 다운로드를 시도합니다...")

            self.model = YOLO(model_name)
            if hasattr(self.model, "names") and len(self.model.names) > 0:
                print("✅ YOLOv12 모델 로드 성공!")
                print(f"사용 모델: {model_name}")
            else:
                    print("모델 로드 완료되었지만 클래스 정보가 비어 있습니다.")

        except Exception as e:
            self.model = None
            print("❌ YOLOv12 모델 로드 실패!")
            print(f"오류 내용: {e}")

    def detect_objects(self, image_path):
        """
        YOLOv12로 객체 탐지 수행
        결과: [{label, confidence, position}] 리스트 반환
        """
        results = self.model(image_path, verbose=False)
        detections = []

        # 인식 결과 bounding box 가져오기
        boxes = results[0].boxes
        img_width = results[0].orig_shape[1]

        # bounding box를 통해 이미지 상에서의 위치 파악하기
        for box in boxes:
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # 인식 결과가 이미지 상의 왼쪽/오른쪽에 있는지 구분
            center_x = (x1 + x2) / 2
            position = "왼쪽" if center_x < img_width / 2 else "오른쪽"

            detections.append({
                "label": label,
                "confidence": round(conf, 2),       # 정확도
                "position": position
            })

        return detections
    
if __name__ == "__main__":
    print("YOLOv12 Detector 테스트 실행 중...")

    detector = YoloV12Detector("yolo12n.pt")

    # 테스트용 이미지 경로 (원하는 이미지 파일 경로로 바꿔주세요)
    test_image = r"C:\Users\kmj564\Downloads\test.png"  # 예시: 로컬 이미지 경로

    if os.path.exists(test_image):
        results = detector.detect_objects(test_image)
        print("\n[결과 출력]")
        for r in results:
            print(f"- {r['label']} ({r['confidence']*100:.1f}%) → {r['position']}")
    else:
        print(f"❌ 테스트 이미지가 존재하지 않습니다: {test_image}")