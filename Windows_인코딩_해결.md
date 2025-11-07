# 🪟 Windows 한글 인코딩 오류 해결 가이드

## 🚨 발생한 오류

```
UnicodeDecodeError: 'cp949' codec can't decode byte 0xec in position 678: illegal multibyte sequence
```

이 오류는 Windows에서 한글이 포함된 파일을 읽을 때 발생하는 인코딩 문제예요.

---

## ✅ 해결 완료!

`train.py` 파일을 자동으로 수정했어요. UTF-8 인코딩을 명시적으로 사용하도록 변경했습니다.

**수정 내용:**
```python
# 이전 (오류 발생)
with open(self.config_path, 'r') as f:

# 수정 후 (정상 작동)
with open(self.config_path, 'r', encoding='utf-8') as f:
```

---

## 🚀 이제 학습하세요!

### 방법 1: 명령어로 실행

```bash
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 10
```

### 방법 2: 배치 파일로 실행 (더 쉬움!)

`학습_시작.bat` 파일을 더블클릭하세요!

또는 명령 프롬프트에서:
```bash
학습_시작.bat
```

그러면 메뉴가 나와요:
```
1. 빠른 테스트 (10 에포크, 약 10-20분)
2. 기본 학습 (50 에포크, 약 1-2시간)
3. 긴 학습 (100 에포크, 약 2-4시간)
4. 커스텀 설정
```

숫자만 입력하면 자동으로 학습이 시작돼요! 😊

---

## 🔧 Windows 명령 프롬프트 설정

Windows에서 한글을 제대로 표시하려면:

### 1. UTF-8 인코딩 활성화

명령 프롬프트에서:
```bash
chcp 65001
```

### 2. 폰트 변경

1. 명령 프롬프트 창 상단 바 우클릭
2. **속성** 선택
3. **글꼴** 탭
4. **맑은 고딕** 또는 **Consolas** 선택

---

## 💡 다른 Python 파일에서 같은 문제가 발생하면?

### 해결 방법:

파일을 열 때 항상 `encoding='utf-8'`을 추가하세요:

**잘못된 예:**
```python
with open('file.txt', 'r') as f:
    content = f.read()
```

**올바른 예:**
```python
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
```

파일을 쓸 때도 마찬가지:
```python
with open('file.txt', 'w', encoding='utf-8') as f:
    f.write('한글 내용')
```

---

## 🎓 왜 이런 오류가 발생하나요?

### Windows의 기본 인코딩

- Windows는 기본적으로 **cp949** (한국어) 또는 **cp1252** (영어) 인코딩 사용
- 하지만 현대 프로그래밍에서는 **UTF-8**이 표준

### 문제 발생 시나리오

1. `config.yaml` 파일에 한글 주석이 있음
2. 파일은 UTF-8로 저장됨
3. Python이 Windows 기본 인코딩(cp949)으로 읽으려고 함
4. UTF-8 바이트를 cp949로 해석하려다 오류 발생

### 해결책

파일을 열 때 `encoding='utf-8'`을 명시하면 해결!

---

## 📋 체크리스트

인코딩 문제가 해결됐는지 확인하세요:

- [ ] `train.py` 파일이 최신 버전인지 확인
- [ ] 명령 프롬프트에서 `chcp 65001` 실행
- [ ] `python train.py --data data/maple-rune-gloxg/data.yaml --epochs 10` 실행
- [ ] 오류 없이 학습이 시작되는지 확인

---

## 🆘 여전히 문제가 있나요?

### 문제 1: "FileNotFoundError"

**원인**: 파일 경로가 잘못됨

**해결**:
```bash
# 현재 위치 확인
cd

# 올바른 폴더로 이동
cd C:\Users\USER\Desktop\autoyolo

# 다시 실행
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 10
```

### 문제 2: "ModuleNotFoundError"

**원인**: 필요한 패키지가 설치되지 않음

**해결**:
```bash
pip install -r requirements.txt
```

### 문제 3: 한글이 깨져 보여요

**해결**:
```bash
# UTF-8 인코딩 활성화
chcp 65001

# 다시 실행
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 10
```

---

## 🎯 빠른 시작 (복사해서 사용하세요!)

```bash
# 1. UTF-8 활성화
chcp 65001

# 2. 의존성 설치 (처음 한 번만)
pip install -r requirements.txt

# 3. 데이터셋 다운로드 (아직 안 했다면)
python easy_download.py "https://universe.roboflow.com/proyecto-kegnn/maple-rune-gloxg/dataset/5"

# 4. 학습 시작
python train.py --data data/maple-rune-gloxg/data.yaml --epochs 10

# 또는 배치 파일 실행
학습_시작.bat
```

---

## 📚 추가 자료

- [Python 공식 문서 - 인코딩](https://docs.python.org/ko/3/howto/unicode.html)
- [Windows 코드 페이지 목록](https://docs.microsoft.com/ko-kr/windows/win32/intl/code-page-identifiers)

---

**문제가 해결됐나요? 이제 학습을 시작하세요!** 🚀
