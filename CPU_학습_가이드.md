# 🖥️ GPU 없이 CPU로 학습하기 (완벽 가이드)

GPU가 없어도 걱정 마세요! CPU로도 충분히 학습할 수 있어요! 🚀

---

## ✅ 해결 완료!

`config.yaml` 파일을 자동으로 수정했어요:
- ✅ `device: 0` → `device: cpu` (CPU 사용)
- ✅ `batch_size: 16` → `batch_size: 8` (CPU에 최적화)
- ✅ `workers: 8` → `workers: 4` (CPU에 최적화)

---

## 🚀 이제 학습 시작!

### 방법 1: 기본 설정으로 학습 (간단!)

```bash
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 50
```

### 방법 2: 더 빠르게 테스트 (추천!)

처음에는 10 에포크로 빠르게 테스트해보세요:

```bash
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 10
```

정상 작동하면 그 다음에 50 에포크로 학습:

```bash
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 50
```

---

## ⏱️ 예상 시간

CPU로 학습하면 시간이 좀 걸려요:

| 에포크 수 | 데이터셋 크기 | 예상 시간 |
|-----------|---------------|-----------|
| 10 에포크 | 100장 | 10-20분 |
| 10 에포크 | 500장 | 30-60분 |
| 50 에포크 | 100장 | 1-2시간 |
| 50 에포크 | 500장 | 3-5시간 |

💡 **팁**: 학습 중에도 컴퓨터를 사용할 수 있어요! 다른 작업 하면서 기다리세요.

---

## 📊 학습 진행 확인

학습이 시작되면 이런 화면이 보여요:

```
Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
  1/50         0G      1.234      0.567      0.890        100        640: 100%|████████| 10/10 [00:15<00:00,  1.5s/it]
  2/50         0G      1.123      0.456      0.789        100        640: 100%|████████| 10/10 [00:14<00:00,  1.4s/it]
  3/50         0G      1.012      0.345      0.678        100        640: 100%|████████| 10/10 [00:14<00:00,  1.4s/it]
```

- `Epoch`: 현재 진행 중인 에포크
- `box_loss`, `cls_loss`: 손실 값 (낮아질수록 좋음)
- 진행률 바가 100%가 되면 1 에포크 완료!

---

## ✅ 학습 완료 확인

학습이 끝나면 이런 메시지가 나와요:

```
Training completed successfully!

Model saved to: models/rune_detection
Best weights: models/rune_detection/weights/best.pt
Last weights: models/rune_detection/weights/last.pt

To use the trained model for detection:
  python detect_rune.py --source <image/video> --model models/rune_detection/weights/best.pt
```

---

## 🎯 학습 완료 후 테스트

### 1. 이미지 파일로 테스트

먼저 테스트할 이미지를 준비하세요 (예: `test.jpg`)

```bash
python detect_rune.py --source test.jpg --model models/rune_detection/weights/best.pt
```

### 2. 웹캠으로 실시간 테스트

```bash
python detect_rune.py --source webcam --model models/rune_detection/weights/best.pt
```

(종료하려면 `q` 키를 누르세요)

### 3. 폴더 안의 모든 이미지 테스트

```bash
python detect_rune.py --source test_images/ --model models/rune_detection/weights/best.pt --output output/results/
```

---

## 🐛 문제 해결

### 문제 1: "CUDA 오류"가 계속 나요

**해결책**: 명령줄에서 직접 CPU를 지정하세요

```bash
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 50 --device cpu
```

### 문제 2: 메모리 부족 오류

**해결책**: 배치 크기를 더 줄이세요

```bash
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 50 --batch 4
```

### 문제 3: 너무 느려요!

**해결책**:
1. 이미지 크기를 줄이세요 (640 → 416)
```bash
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 50 --img-size 416
```

2. 더 작은 모델을 사용하세요
```bash
# yolo12n은 이미 가장 작은 모델이에요!
# 더 빠르게 하려면 에포크를 줄이세요
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 20
```

### 문제 4: "data.yaml을 찾을 수 없어요"

**해결책**: 경로를 확인하세요

Windows에서:
```bash
# 현재 위치 확인
cd

# data 폴더 확인
dir data

# maple-rune-gloxg 폴더 확인
dir data\maple-rune-gloxg

# data.yaml 파일 확인
type data\maple-rune-gloxg\data.yaml
```

---

## 💡 CPU 학습 최적화 팁

### 1. 작은 데이터셋부터 시작

전체 데이터셋이 크면 일부만 사용해서 먼저 테스트:
```bash
# 학습 이미지 100장만 사용
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 10
```

### 2. 학습 중 다른 프로그램 종료

- 크롬, 게임, 영상 편집 프로그램 등을 닫으세요
- 메모리와 CPU를 최대한 확보하세요

### 3. 전원 옵션 설정

Windows:
1. 설정 → 시스템 → 전원 및 배터리
2. 전원 모드: **최고 성능**으로 설정

### 4. 백그라운드에서 실행

학습이 오래 걸리면 백그라운드로 실행:
```bash
# Windows에서는 새 터미널 창에서 실행하고 최소화
```

---

## 📈 학습 결과 확인

학습이 끝나면 `models/rune_detection` 폴더에 여러 파일이 생성돼요:

```
models/rune_detection/
├── weights/
│   ├── best.pt          ← 가장 좋은 모델 (이걸 사용!)
│   └── last.pt          ← 마지막 모델
├── results.png          ← 학습 그래프
├── confusion_matrix.png ← 혼동 행렬
└── ...
```

### 그래프 보기:

```bash
# Windows 탐색기로 열기
explorer models\rune_detection
```

`results.png`를 열어보면:
- Loss 그래프 (낮아지는 게 좋음)
- mAP 그래프 (높아지는 게 좋음)

---

## 🎯 완벽한 학습 체크리스트

- [ ] `config.yaml`에서 `device: cpu` 확인
- [ ] 데이터셋 다운로드 완료 (`data/maple-rune-gloxg/`)
- [ ] `data.yaml` 파일 존재 확인
- [ ] 다른 프로그램 종료
- [ ] 학습 시작: `python train.py --data data/maple-rune-gloxg/data.yaml --epochs 10`
- [ ] 학습 진행 중 (손실 값 감소 확인)
- [ ] 학습 완료 (`best.pt` 파일 생성)
- [ ] 테스트 이미지로 검증
- [ ] 결과 만족하면 더 많은 에포크로 재학습

---

## 🚀 다음 단계

학습이 잘 되면:

1. **더 긴 학습**:
```bash
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 100
```

2. **더 큰 모델** (더 정확하지만 느림):
```bash
python train.py --data data/maple-rune-gloxg/data.yaml --model yolo12s --epochs 50
```

3. **실전 적용**:
- 웹캠으로 실시간 감지
- 비디오 파일 분석
- 대량의 이미지 처리

---

**이제 학습을 시작하세요! 화이팅! 💪**

궁금한 점이 있으면 언제든 물어보세요! 😊
