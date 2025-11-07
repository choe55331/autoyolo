# 🚀 학습 데이터를 GitHub에 업로드하는 방법

## 📊 현재 상황

`.gitignore` 설정으로 다음이 **제외**되어 있어요:
- ✅ `data/` - 데이터셋 폴더
- ✅ `models/` - 학습된 모델 폴더
- ✅ `*.pt` - 모델 파일들
- ✅ `output/` - 결과 폴더

**이건 의도적인 설정**이에요! 왜냐하면:
- GitHub는 파일당 100MB 제한
- 데이터셋과 모델은 보통 수백 MB ~ 수 GB
- 저장소가 느려지고 관리가 어려워짐

---

## 🎯 방법 1: Git LFS (Large File Storage) - 제한적

### Git LFS란?

Git LFS는 큰 파일을 효율적으로 관리하는 Git 확장 프로그램이에요.

### 제한사항 (무료 계정)
- 저장공간: **1GB**
- 대역폭: **1GB/월**
- 초과 시 추가 비용 발생

### 설치 및 사용

#### 1. Git LFS 설치

**Windows:**
```bash
# Git for Windows 설치 시 포함됨
# 또는 https://git-lfs.github.com/ 에서 다운로드
git lfs install
```

**Mac:**
```bash
brew install git-lfs
git lfs install
```

**Linux:**
```bash
sudo apt install git-lfs  # Ubuntu/Debian
git lfs install
```

#### 2. 추적할 파일 설정

```bash
# 모델 파일 추적
git lfs track "*.pt"
git lfs track "*.pth"
git lfs track "*.weights"

# 큰 이미지 파일 추적 (선택적)
git lfs track "*.jpg"
git lfs track "*.png"

# .gitattributes 파일 커밋
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

#### 3. .gitignore 수정

```bash
# .gitignore 편집
nano .gitignore
```

다음 줄을 **제거하거나 주석 처리**:
```
# data/         ← 이 줄을 주석 처리 또는 제거
# models/       ← 이 줄을 주석 처리 또는 제거
# *.pt          ← 이 줄을 주석 처리 또는 제거
```

#### 4. 파일 추가 및 커밋

```bash
# 모델 파일 추가
git add models/rune_detection/weights/best.pt
git commit -m "Add trained model"

# 데이터셋 추가 (주의: 크기 확인!)
git add data/maple-rune-gloxg/
git commit -m "Add training dataset"

# 푸시
git push
```

#### ⚠️ 주의사항
- 파일 크기를 미리 확인하세요!
- 1GB 제한을 초과하지 마세요

```bash
# 폴더 크기 확인 (Windows)
dir /s data\maple-rune-gloxg

# 파일 크기 확인 (Linux/Mac)
du -sh data/maple-rune-gloxg
du -sh models/rune_detection/weights/best.pt
```

---

## 🎯 방법 2: 외부 저장소 사용 (추천!) ⭐

큰 파일은 외부에 저장하고, GitHub에는 **다운로드 스크립트**만 올리세요!

### 옵션 A: Google Drive

**장점**:
- 무료 15GB
- 쉬운 사용
- 빠른 다운로드

**단계:**

1. **Google Drive에 업로드**
   - https://drive.google.com 접속
   - 폴더 만들기: `autoyolo-models`
   - `best.pt` 파일 업로드

2. **공유 링크 만들기**
   - 파일 우클릭 → 공유
   - "링크가 있는 모든 사용자" 선택
   - 링크 복사

3. **README에 링크 추가**
   ```markdown
   ## 학습된 모델 다운로드

   [Google Drive에서 다운로드](https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing)

   다운로드 후 `models/rune_detection/weights/` 폴더에 넣으세요.
   ```

4. **자동 다운로드 스크립트 만들기**
   - 아래 "다운로드 스크립트" 섹션 참고

### 옵션 B: Hugging Face Hub (AI/ML 특화)

**장점**:
- AI/ML 모델에 특화
- 무료 무제한 저장
- 버전 관리
- 커뮤니티 공유 쉬움

**단계:**

1. **Hugging Face 계정 생성**
   - https://huggingface.co 접속
   - 무료 회원가입

2. **저장소 생성**
   - New → Model
   - 이름: `maple-rune-detection`

3. **모델 업로드**
   ```bash
   # Hugging Face CLI 설치
   pip install huggingface-hub

   # 로그인
   huggingface-cli login

   # 모델 업로드
   huggingface-cli upload your-username/maple-rune-detection models/rune_detection/weights/best.pt
   ```

4. **다운로드 스크립트**
   ```python
   from huggingface_hub import hf_hub_download

   model_path = hf_hub_download(
       repo_id="your-username/maple-rune-detection",
       filename="best.pt",
       local_dir="models/rune_detection/weights/"
   )
   ```

### 옵션 C: GitHub Releases (100MB 미만 파일만)

**장점**:
- GitHub 내에서 관리
- 버전별로 파일 관리

**단계:**

1. **GitHub 저장소 페이지로 이동**
2. **Releases** 탭 클릭
3. **Create a new release** 클릭
4. 태그: `v1.0`
5. **Attach binaries** 클릭
6. 모델 파일(100MB 미만) 업로드
7. **Publish release**

다운로드:
```bash
wget https://github.com/username/autoyolo/releases/download/v1.0/best.pt -O models/rune_detection/weights/best.pt
```

### 옵션 D: Roboflow (데이터셋)

**장점**:
- 데이터셋 관리에 특화
- 자동 변환 및 증강

**단계:**

1. Roboflow에 이미 업로드된 데이터셋 사용
2. README에 다운로드 명령어 추가:
   ```bash
   python easy_download.py "https://universe.roboflow.com/proyecto-kegnn/maple-rune-gloxg/dataset/5"
   ```

---

## 🎯 방법 3: 작은 데모만 포함 (가장 실용적!)

전체 데이터가 아닌 **샘플 데이터**만 GitHub에 포함하세요!

### 단계:

1. **샘플 폴더 생성**
   ```bash
   mkdir data/samples
   ```

2. **대표 이미지 몇 개만 복사** (5-10장)
   ```bash
   # Windows
   copy data\maple-rune-gloxg\train\images\image1.jpg data\samples\
   copy data\maple-rune-gloxg\train\images\image2.jpg data\samples\

   # Linux/Mac
   cp data/maple-rune-gloxg/train/images/image1.jpg data/samples/
   ```

3. **.gitignore 수정**
   ```
   # Data and models
   data/*
   !data/samples/
   !data/.gitkeep
   models/
   !models/.gitkeep
   ```

4. **커밋**
   ```bash
   git add data/samples/
   git commit -m "Add sample images for demo"
   git push
   ```

---

## 📝 다운로드 스크립트 만들기

외부 저장소를 사용한다면, 자동 다운로드 스크립트를 만드세요!

### download_models.py

```python
#!/usr/bin/env python3
"""학습된 모델 자동 다운로드"""

import os
import urllib.request
from pathlib import Path

# Google Drive 파일 ID
GOOGLE_DRIVE_FILE_ID = "YOUR_FILE_ID_HERE"

# 저장 경로
SAVE_PATH = "models/rune_detection/weights/best.pt"

def download_from_google_drive(file_id, destination):
    """Google Drive에서 파일 다운로드"""
    URL = f"https://drive.google.com/uc?export=download&id={file_id}"

    print(f"다운로드 중: {destination}")

    # 폴더 생성
    Path(destination).parent.mkdir(parents=True, exist_ok=True)

    # 다운로드
    urllib.request.urlretrieve(URL, destination)

    print("✅ 다운로드 완료!")

if __name__ == "__main__":
    if not os.path.exists(SAVE_PATH):
        print("학습된 모델을 다운로드합니다...")
        download_from_google_drive(GOOGLE_DRIVE_FILE_ID, SAVE_PATH)
    else:
        print("✅ 모델이 이미 존재합니다.")
```

### download_models.bat (Windows용)

```batch
@echo off
echo 학습된 모델 다운로드 중...
python download_models.py
if %errorlevel% equ 0 (
    echo ✅ 다운로드 완료!
) else (
    echo ❌ 다운로드 실패
)
pause
```

---

## 📋 완벽한 워크플로우 (추천)

### GitHub에 포함할 것:
- ✅ 소스 코드 (`.py`, `.bat` 파일)
- ✅ 설정 파일 (`config.yaml`)
- ✅ 문서 (`README.md`, 가이드)
- ✅ 다운로드 스크립트
- ✅ 샘플 이미지 (5-10장)
- ✅ `.gitignore`, `requirements.txt`

### 외부에 저장할 것:
- 📦 전체 데이터셋 → Roboflow 또는 Google Drive
- 🤖 학습된 모델 → Hugging Face 또는 Google Drive

### README.md에 추가할 내용:

```markdown
## 📦 데이터셋 다운로드

```bash
python easy_download.py "https://universe.roboflow.com/proyecto-kegnn/maple-rune-gloxg/dataset/5"
```

## 🤖 학습된 모델 다운로드

### 방법 1: 자동 다운로드 (추천)
```bash
python download_models.py
```

### 방법 2: 수동 다운로드
1. [Google Drive 링크](https://drive.google.com/file/d/YOUR_ID/view)에서 `best.pt` 다운로드
2. `models/rune_detection/weights/` 폴더에 복사
```

---

## 🎯 실전 예제

### 시나리오: 모델을 Google Drive에 업로드하고 GitHub에서 사용

#### 1. Google Drive에 업로드

1. https://drive.google.com 접속
2. 새 폴더: `autoyolo-models`
3. `best.pt` 파일 업로드
4. 공유 → "링크가 있는 모든 사용자" → 링크 복사

#### 2. 파일 ID 추출

링크:
```
https://drive.google.com/file/d/1a2B3c4D5e6F7g8H9i0J/view?usp=sharing
                                ↑ 이 부분이 File ID
```

File ID: `1a2B3c4D5e6F7g8H9i0J`

#### 3. download_models.py 수정

```python
GOOGLE_DRIVE_FILE_ID = "1a2B3c4D5e6F7g8H9i0J"  # 여기에 실제 ID 입력
```

#### 4. Git에 커밋

```bash
git add download_models.py
git commit -m "Add model download script"
git push
```

#### 5. 다른 사람이 사용

```bash
# 저장소 클론
git clone https://github.com/username/autoyolo.git
cd autoyolo

# 의존성 설치
pip install -r requirements.txt

# 모델 다운로드
python download_models.py

# 학습 또는 테스트
python detect_rune.py --source test.jpg --model models/rune_detection/weights/best.pt
```

---

## 💡 최종 추천

### 당신의 경우 (Maple Rune 프로젝트):

1. **데이터셋**:
   - Roboflow에 이미 있으니 그대로 사용
   - `easy_download.py` 스크립트로 다운로드

2. **학습된 모델**:
   - Google Drive 또는 Hugging Face에 업로드
   - `download_models.py` 스크립트로 자동 다운로드

3. **GitHub에는**:
   - 소스 코드, 문서, 스크립트만 포함
   - 샘플 이미지 5-10장만 포함

4. **README에**:
   - 데이터셋 다운로드 방법
   - 모델 다운로드 링크
   - 빠른 시작 가이드

---

어떤 방법을 사용하고 싶으세요? 제가 도와드릴게요! 😊
