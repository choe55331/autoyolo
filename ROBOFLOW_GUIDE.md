# Roboflow 데이터셋 다운로드 가이드

## 📚 목차
1. [Roboflow 계정 생성 및 API 키 받기](#1-roboflow-계정-생성-및-api-키-받기)
2. [데이터셋 찾기](#2-데이터셋-찾기)
3. [데이터셋 정보 확인](#3-데이터셋-정보-확인)
4. [스크립트로 다운로드](#4-스크립트로-다운로드)
5. [실전 예제](#5-실전-예제)

---

## 1. Roboflow 계정 생성 및 API 키 받기

### 1-1. 계정 생성
1. [Roboflow 웹사이트](https://roboflow.com/) 접속
2. 우측 상단 **Sign Up** 버튼 클릭
3. 이메일 또는 Google 계정으로 가입
4. 무료 플랜으로 시작 가능 (월 1000장 무료)

### 1-2. API 키 받기
1. 로그인 후 우측 상단 프로필 클릭
2. **Settings** 또는 **Account** 메뉴 선택
3. 좌측 메뉴에서 **Roboflow API** 클릭
4. **Private API Key** 복사 (예: `xxxxxxxxxxxxxxxxxxx`)

```bash
# API 키를 환경변수로 설정 (추천)
export ROBOFLOW_API_KEY="your_api_key_here"

# 또는 .env 파일에 저장
echo "ROBOFLOW_API_KEY=your_api_key_here" > .env
```

---

## 2. 데이터셋 찾기

Roboflow에서 데이터셋을 찾는 방법은 2가지입니다:

### 방법 A: Roboflow Universe에서 공개 데이터셋 사용

1. [Roboflow Universe](https://universe.roboflow.com/) 접속
2. 검색창에서 원하는 키워드 검색 (예: "rune", "symbol", "character")
3. 필터 적용:
   - **Models**: Object Detection 선택
   - **Format**: YOLOv8 (YOLO12와 호환됨)
4. 마음에 드는 데이터셋 클릭

### 방법 B: 자신의 데이터셋 생성 (커스텀)

1. Roboflow 대시보드에서 **Create New Project** 클릭
2. 프로젝트 이름 입력 (예: "my-rune-detection")
3. **Annotation Group**: Object Detection 선택
4. 이미지 업로드 및 라벨링
5. Generate → Export

---

## 3. 데이터셋 정보 확인

데이터셋을 다운로드하려면 다음 3가지 정보가 필요합니다:

### 필요한 정보:
1. **Workspace** (작업공간 이름)
2. **Project** (프로젝트 이름)
3. **Version** (데이터셋 버전 번호)

### Universe 데이터셋에서 정보 찾기:

데이터셋 페이지의 URL을 확인하세요:
```
https://universe.roboflow.com/[workspace]/[project]/[version]
```

**예시:**
```
https://universe.roboflow.com/joseph-nelson/bccd/2
```
- Workspace: `joseph-nelson`
- Project: `bccd`
- Version: `2`

### 자신의 프로젝트에서 정보 찾기:

1. Roboflow 대시보드에서 프로젝트 클릭
2. 좌측 메뉴에서 **Versions** 클릭
3. 원하는 버전 선택
4. URL 확인:
```
https://app.roboflow.com/[workspace]/[project]/[version]
```

---

## 4. 스크립트로 다운로드

### 방법 1: roboflow_integration.py 사용 (추천)

```bash
# 기본 다운로드
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    download \
    --workspace joseph-nelson \
    --project bccd \
    --version 2

# 다운로드 위치 지정
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    download \
    --workspace joseph-nelson \
    --project bccd \
    --version 2 \
    --location ./data/bccd

# 다른 포맷 (기본은 yolov8)
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    download \
    --workspace joseph-nelson \
    --project bccd \
    --version 2 \
    --format yolov8
```

### 방법 2: Python 코드로 직접 다운로드

```python
from roboflow import Roboflow

# 1. Roboflow 클라이언트 초기화
rf = Roboflow(api_key="YOUR_API_KEY")

# 2. 프로젝트 가져오기
project = rf.workspace("workspace-name").project("project-name")

# 3. 특정 버전 선택
dataset = project.version(1)

# 4. 다운로드
dataset.download("yolov8", location="./data")
```

---

## 5. 실전 예제

### 예제 1: Universe의 공개 데이터셋 사용

**시나리오**: Playing Cards 데이터셋으로 카드 인식 학습

```bash
# 1. 데이터셋 정보
# URL: https://universe.roboflow.com/augmented-startups/playing-cards-ow27d/4
# Workspace: augmented-startups
# Project: playing-cards-ow27d
# Version: 4

# 2. 다운로드
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    download \
    --workspace augmented-startups \
    --project playing-cards-ow27d \
    --version 4 \
    --location ./data/playing-cards

# 3. config.yaml 수정
# dataset:
#   data_yaml: data/playing-cards/data.yaml

# 4. 학습
python train.py --data data/playing-cards/data.yaml --epochs 50
```

### 예제 2: Rune 관련 데이터셋 찾고 다운로드

```bash
# 1. Universe에서 "rune" 검색
# 예: https://universe.roboflow.com/user-xxx/rune-detection/1

# 2. 먼저 프로젝트 목록 확인 (선택사항)
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    list \
    --workspace user-xxx

# 3. 데이터셋 정보 확인 (선택사항)
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    info \
    --workspace user-xxx \
    --project rune-detection \
    --version 1

# 4. 다운로드
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    download \
    --workspace user-xxx \
    --project rune-detection \
    --version 1 \
    --location ./data/runes

# 5. 다운로드 확인
ls -la ./data/runes
# train/ val/ test/ data.yaml README.dataset.txt README.roboflow.txt
```

### 예제 3: 자신의 데이터셋 다운로드

```bash
# 1. Roboflow에서 이미지 업로드 및 라벨링 완료
# 2. Generate → Train/Valid/Test split 설정 (70/20/10)
# 3. Export → Format: YOLOv8 선택

# 4. 자신의 workspace 이름 확인
# URL: https://app.roboflow.com/[your-workspace]/...

# 5. 다운로드
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    download \
    --workspace your-workspace \
    --project my-rune-project \
    --version 1 \
    --location ./data/my-runes
```

---

## 💡 유용한 팁

### Tip 1: 환경변수로 API 키 관리

매번 API 키를 입력하지 않으려면:

```bash
# .bashrc 또는 .zshrc에 추가
export ROBOFLOW_API_KEY="your_api_key"

# 스크립트 수정해서 환경변수에서 읽기
import os
api_key = os.getenv('ROBOFLOW_API_KEY')
```

### Tip 2: 다운로드한 데이터셋 구조

```
data/dataset-name/
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
├── test/
│   ├── images/
│   └── labels/
├── data.yaml          # YOLO 학습에 필요한 설정 파일
└── README.roboflow.txt
```

### Tip 3: data.yaml 내용 확인

```bash
cat data/dataset-name/data.yaml
```

출력 예시:
```yaml
train: ./train/images
val: ./valid/images
test: ./test/images

nc: 5  # number of classes
names: ['class1', 'class2', 'class3', 'class4', 'class5']
```

### Tip 4: 데이터셋 포맷

사용 가능한 포맷:
- `yolov8` (추천 - YOLO12와 호환)
- `yolov5`
- `coco`
- `voc`
- `tensorflow`
- 등등

---

## 🔧 트러블슈팅

### 문제 1: API 키 오류
```
Error: Invalid API key
```

**해결:**
1. API 키가 정확한지 확인
2. Roboflow 웹사이트에서 키 재확인
3. 따옴표로 키를 감싸기: `--api-key "your_key"`

### 문제 2: 프로젝트를 찾을 수 없음
```
Error: Project not found
```

**해결:**
1. Workspace, Project, Version 이름 확인
2. Universe 데이터셋의 경우: 자신의 workspace에 먼저 fork 필요
3. URL에서 정확한 이름 복사 (대소문자 구분)

### 문제 3: 다운로드가 느림

**해결:**
1. 안정적인 인터넷 연결 확인
2. 큰 데이터셋의 경우 시간이 걸릴 수 있음
3. 필요한 경우 버전을 나눠서 다운로드

### 문제 4: 권한 오류
```
Error: You don't have access to this dataset
```

**해결:**
1. Public 데이터셋인지 확인
2. Private 데이터셋은 소유자가 접근 권한을 부여해야 함
3. Universe에서 먼저 "Fork to Workspace" 클릭

---

## 📖 추가 리소스

- [Roboflow 공식 문서](https://docs.roboflow.com/)
- [Roboflow Universe](https://universe.roboflow.com/)
- [Python SDK 문서](https://docs.roboflow.com/python)
- [YouTube 튜토리얼](https://www.youtube.com/@Roboflow)

---

## 🎯 빠른 시작 체크리스트

- [ ] Roboflow 계정 생성
- [ ] API 키 복사
- [ ] Universe에서 데이터셋 찾기 또는 직접 생성
- [ ] Workspace, Project, Version 정보 확인
- [ ] `roboflow_integration.py`로 다운로드
- [ ] `data.yaml` 경로 확인
- [ ] `config.yaml` 업데이트
- [ ] `train.py`로 학습 시작!

---

**문제가 있으면 언제든지 질문하세요!** 🚀
