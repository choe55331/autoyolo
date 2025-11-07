# AutoYOLO - YOLO12 Rune Detection

YOLO12를 사용한 실시간 Rune 인식 프로그램입니다. Roboflow와 통합되어 쉽게 데이터셋을 다운로드하고 학습할 수 있습니다.

## 🚀 주요 기능

- **YOLO12 모델**: 최신 YOLOv12 아키텍처 사용
- **다중 입력 지원**: 이미지, 비디오, 웹캠 실시간 감지
- **Roboflow 통합**: 간편한 데이터셋 다운로드 및 관리
- **커스텀 학습**: 자신만의 rune 데이터셋으로 모델 학습
- **설정 가능**: YAML 기반 설정 파일로 쉬운 파라미터 조정

## 📋 요구사항

- Python 3.8 이상
- CUDA 지원 GPU (학습 시 권장)
- 웹캠 (실시간 감지 시)

## 🔧 설치

1. 저장소 클론:
```bash
git clone <repository-url>
cd autoyolo
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

## 📦 프로젝트 구조

```
autoyolo/
├── detect_rune.py           # Rune 감지 메인 스크립트
├── train.py                 # 모델 학습 스크립트
├── roboflow_integration.py  # Roboflow 데이터셋 관리
├── config.yaml              # 설정 파일
├── requirements.txt         # Python 의존성
├── models/                  # 학습된 모델 저장 디렉토리
├── data/                    # 데이터셋 디렉토리
│   ├── train/
│   ├── val/
│   └── test/
└── output/                  # 결과 저장 디렉토리
    ├── images/
    └── videos/
```

## 🎯 사용법

### 1. Roboflow에서 데이터셋 다운로드

먼저 [Roboflow](https://roboflow.com/)에서 API 키를 받으세요.

```bash
# 프로젝트 목록 확인
python roboflow_integration.py --api-key YOUR_API_KEY list --workspace your-workspace

# 데이터셋 다운로드
python roboflow_integration.py --api-key YOUR_API_KEY download \
    --workspace your-workspace \
    --project rune-detection \
    --version 1 \
    --location ./data
```

### 2. 설정 파일 수정

`config.yaml` 파일을 열어 설정을 수정하세요:

```yaml
# 모델 아키텍처 선택 (yolo12n, yolo12s, yolo12m, yolo12l, yolo12x)
model:
  architecture: yolo12n

# 데이터셋 경로 설정
dataset:
  data_yaml: data/your-dataset/data.yaml

# Roboflow 설정
roboflow:
  workspace: your-workspace
  project: rune-detection
  version: 1
```

### 3. 모델 학습

```bash
# 기본 설정으로 학습
python train.py

# 커스텀 설정으로 학습
python train.py --epochs 100 --batch 16 --img-size 640

# 특정 데이터셋으로 학습
python train.py --data data/my-dataset/data.yaml --model yolo12s
```

학습이 완료되면 모델은 `models/rune_detection/weights/best.pt`에 저장됩니다.

### 4. Rune 감지

#### 이미지에서 감지:
```bash
python detect_rune.py --source image.jpg --model models/best.pt
```

#### 비디오에서 감지:
```bash
python detect_rune.py --source video.mp4 --model models/best.pt --output output/result.mp4
```

#### 웹캠 실시간 감지:
```bash
python detect_rune.py --source webcam --model models/best.pt
```

#### 고급 옵션:
```bash
# 신뢰도 임계값 조정
python detect_rune.py --source image.jpg --conf 0.5

# IoU 임계값 조정
python detect_rune.py --source image.jpg --iou 0.5

# 결과 표시 안 함 (백그라운드 처리)
python detect_rune.py --source video.mp4 --output result.mp4 --no-show

# 다른 카메라 사용
python detect_rune.py --source webcam --camera-id 1
```

### 5. 모델 검증

```bash
# 학습된 모델 검증
python train.py --validate --model-path models/rune_detection/weights/best.pt
```

## 🎨 Roboflow Universe 활용

[Roboflow Universe](https://universe.roboflow.com/models/object-detection)에서 다양한 사전 학습된 object detection 모델을 찾을 수 있습니다:

1. Universe에서 원하는 데이터셋 찾기
2. 데이터셋 정보 확인 (workspace, project, version)
3. `roboflow_integration.py`로 다운로드
4. `train.py`로 fine-tuning

## 📊 모델 성능

YOLO12 모델은 다양한 크기로 제공됩니다:

| 모델 | 크기 | 속도 | 정확도 | 용도 |
|------|------|------|--------|------|
| yolo12n | Nano | 빠름 | 중간 | 실시간, 임베디드 |
| yolo12s | Small | 빠름 | 좋음 | 실시간 |
| yolo12m | Medium | 중간 | 매우 좋음 | 균형 |
| yolo12l | Large | 느림 | 우수 | 높은 정확도 |
| yolo12x | XLarge | 매우 느림 | 최고 | 최고 정확도 |

## ⚙️ 설정 옵션

### 감지 설정
- `conf_threshold`: 신뢰도 임계값 (0.0-1.0)
- `iou_threshold`: NMS IoU 임계값 (0.0-1.0)
- `max_det`: 이미지당 최대 감지 수

### 학습 설정
- `epochs`: 학습 에포크 수
- `batch_size`: 배치 크기
- `img_size`: 입력 이미지 크기
- `learning_rate`: 학습률
- `optimizer`: 최적화 알고리즘 (SGD, Adam, AdamW)
- `device`: 계산 장치 (cpu, 0, 0,1,2,3)

자세한 설정은 `config.yaml`을 참조하세요.

## 🐛 트러블슈팅

### CUDA Out of Memory
```bash
# 배치 크기 줄이기
python train.py --batch 8

# 더 작은 모델 사용
python train.py --model yolo12n
```

### 데이터셋을 찾을 수 없음
- `config.yaml`의 `data_yaml` 경로 확인
- 데이터셋이 제대로 다운로드되었는지 확인

### 웹캠이 작동하지 않음
```bash
# 다른 카메라 ID 시도
python detect_rune.py --source webcam --camera-id 1
```

## 📝 예제

### 빠른 시작 예제

```bash
# 1. 데이터셋 다운로드
python roboflow_integration.py --api-key YOUR_KEY download \
    --workspace example --project runes --version 1

# 2. 모델 학습 (10 에포크로 테스트)
python train.py --epochs 10 --batch 8

# 3. 테스트 이미지로 감지
python detect_rune.py --source data/test/image.jpg --model models/rune_detection/weights/best.pt
```

## 🤝 기여

이슈나 풀 리퀘스트를 환영합니다!

## 📄 라이선스

MIT License

## 🙏 감사의 말

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) - YOLO 구현
- [Roboflow](https://roboflow.com/) - 데이터셋 관리 플랫폼

## 📧 문의

문제가 있거나 질문이 있으시면 이슈를 열어주세요.

---

**Happy Rune Detecting! 🔮**
