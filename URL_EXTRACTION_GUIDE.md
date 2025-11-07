# Roboflow URL에서 정보 추출하는 방법 (완전 초보자 가이드)

## 🎯 왜 URL에서 정보를 추출해야 하나요?

Roboflow에서 데이터셋을 다운로드하려면 **3가지 정보**가 필요합니다:
1. **Workspace** (작업공간 이름)
2. **Project** (프로젝트 이름)
3. **Version** (버전 번호)

이 정보들은 **웹사이트 URL 안에 숨어 있습니다!** URL을 보고 이 정보를 찾아내는 방법을 알려드리겠습니다.

---

## 📋 Step 1: Roboflow Universe 웹사이트 방문

1. 웹브라우저를 열고 https://universe.roboflow.com 접속
2. 검색창이 보입니다
3. 원하는 키워드를 검색합니다 (예: "playing cards", "vehicle", "face detection")

---

## 📋 Step 2: 데이터셋 선택하기

검색 결과에서 마음에 드는 데이터셋을 클릭하면, 브라우저 주소창의 URL이 이렇게 보입니다:

```
https://universe.roboflow.com/augmented-startups/playing-cards-ow27d/4
```

이 URL이 바로 우리가 분석해야 할 대상입니다!

---

## 🔍 Step 3: URL 구조 이해하기

URL은 다음과 같은 **규칙적인 패턴**으로 구성됩니다:

```
https://universe.roboflow.com/[workspace]/[project]/[version]
                                   ↓           ↓         ↓
                              작업공간 이름  프로젝트 이름  버전
```

### 실제 예제로 분해해보기:

```
https://universe.roboflow.com/augmented-startups/playing-cards-ow27d/4
                                        ↓                  ↓          ↓
                                  Workspace          Project     Version
```

**추출된 정보:**
- Workspace: `augmented-startups`
- Project: `playing-cards-ow27d`
- Version: `4`

---

## 💡 더 많은 예제로 연습하기

### 예제 1: 혈구 감지 데이터셋

**URL:**
```
https://universe.roboflow.com/joseph-nelson/bccd/2
```

**URL 분석:**
```
https://universe.roboflow.com/joseph-nelson/bccd/2
                                     ↓          ↓   ↓
                               Workspace   Project Version
```

**추출 결과:**
```python
workspace = "joseph-nelson"
project = "bccd"
version = 2
```

**다운로드 명령어:**
```bash
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    download \
    --workspace joseph-nelson \
    --project bccd \
    --version 2
```

---

### 예제 2: 자동차 감지 데이터셋

**URL:**
```
https://universe.roboflow.com/roboflow-100/vehicles-q0a2x/2
```

**URL 분석:**
```
https://universe.roboflow.com / roboflow-100 / vehicles-q0a2x / 2
                                      ↓              ↓          ↓
                                 Workspace       Project    Version
```

**추출 결과:**
```
workspace = "roboflow-100"
project = "vehicles-q0a2x"
version = 2
```

**다운로드 명령어:**
```bash
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    download \
    --workspace roboflow-100 \
    --project vehicles-q0a2x \
    --version 2
```

---

### 예제 3: 안전모 감지 데이터셋

**URL:**
```
https://universe.roboflow.com/my-workspace-abc123/hard-hat-detection/1
```

**URL 분석:**
```
                          [1]              [2]               [3]
https://universe.roboflow.com/my-workspace-abc123/hard-hat-detection/1
                                      ↓                  ↓            ↓
                                 Workspace           Project      Version
```

**추출 결과:**
```
workspace = "my-workspace-abc123"
project = "hard-hat-detection"
version = 1
```

---

## 🎓 URL 읽는 방법 - 단계별 가이드

### 1단계: URL을 슬래시(/)로 나누기

원본 URL:
```
https://universe.roboflow.com/augmented-startups/playing-cards-ow27d/4
```

슬래시로 나눈 결과:
```
https:
(빈 문자열)
universe.roboflow.com
augmented-startups      ← 이것이 Workspace!
playing-cards-ow27d     ← 이것이 Project!
4                       ← 이것이 Version!
```

### 2단계: 위치 파악

```
위치:    [0]   [1]  [2]                [3]                 [4]                [5]
내용:   https  ""   universe...       workspace          project            version
        ↓      ↓    ↓                   ↓                   ↓                  ↓
URL:   https  :   //  universe.roboflow.com / augmented-startups / playing-cards-ow27d / 4
```

**기억하세요:**
- **4번째 위치** = Workspace
- **5번째 위치** = Project
- **6번째 위치** = Version

### 3단계: 정보 추출

```python
# Python으로 자동 추출하기
url = "https://universe.roboflow.com/augmented-startups/playing-cards-ow27d/4"
parts = url.split('/')

workspace = parts[3]  # "augmented-startups"
project = parts[4]    # "playing-cards-ow27d"
version = parts[5]    # "4"
```

---

## 🛠️ 실전 연습: 당신의 URL 분석하기

### 템플릿 사용하기

당신의 URL이 이렇다면:
```
https://universe.roboflow.com/AAAA/BBBB/C
```

다음과 같이 치환하세요:
```python
workspace = "AAAA"
project = "BBBB"
version = C  # 숫자
```

다운로드 명령어:
```bash
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    download \
    --workspace AAAA \
    --project BBBB \
    --version C
```

---

## 📸 실제 화면에서 찾는 방법

### 방법 1: URL 복사하기

1. Roboflow Universe에서 데이터셋 페이지 열기
2. 브라우저 **주소창** 클릭
3. **전체 URL 복사** (Ctrl+C 또는 Cmd+C)
4. 텍스트 에디터에 붙여넣기
5. 슬래시(/)로 구분해서 정보 찾기

### 방법 2: 웹페이지에서 직접 확인

데이터셋 페이지를 보면 이런 정보가 표시됩니다:

```
Dataset: playing-cards-ow27d        ← 이것이 Project
By: augmented-startups              ← 이것이 Workspace
Version: 4                          ← 이것이 Version
```

---

## 🚨 자주 하는 실수들

### 실수 1: 잘못된 부분 복사
❌ **잘못된 예:**
```
workspace = "universe.roboflow.com"  # 이건 도메인입니다!
```

✅ **올바른 예:**
```
workspace = "augmented-startups"  # 도메인 다음에 나오는 이름!
```

### 실수 2: 슬래시 포함
❌ **잘못된 예:**
```
project = "/playing-cards-ow27d/"  # 슬래시가 포함됨
```

✅ **올바른 예:**
```
project = "playing-cards-ow27d"  # 슬래시 없이 이름만
```

### 실수 3: 대소문자 구분 안 함
❌ **잘못된 예:**
```
workspace = "Augmented-Startups"  # 대문자 S
```

✅ **올바른 예:**
```
workspace = "augmented-startups"  # URL과 정확히 동일하게!
```

### 실수 4: 버전을 문자열로 입력
❌ **잘못된 예:**
```bash
--version "4"  # 따옴표 불필요
```

✅ **올바른 예:**
```bash
--version 4  # 숫자 그대로
```

---

## 🎯 전체 프로세스 요약

```
1. Universe 방문
   ↓
2. 데이터셋 검색
   ↓
3. 데이터셋 클릭
   ↓
4. 주소창 URL 복사
   ↓
5. URL 분석:
   https://universe.roboflow.com/[workspace]/[project]/[version]
   ↓
6. 정보 추출:
   workspace = "..."
   project = "..."
   version = 숫자
   ↓
7. 다운로드 명령어 작성:
   python roboflow_integration.py \
       --api-key YOUR_KEY \
       download \
       --workspace [복사한값] \
       --project [복사한값] \
       --version [숫자]
```

---

## 💻 자동 추출 도구

URL을 입력하면 자동으로 정보를 추출해주는 스크립트:

```python
# extract_url_info.py
def extract_roboflow_info(url):
    """
    Roboflow URL에서 workspace, project, version 추출

    예제:
    url = "https://universe.roboflow.com/joseph-nelson/bccd/2"
    extract_roboflow_info(url)
    # 출력: workspace=joseph-nelson, project=bccd, version=2
    """
    # URL을 /로 분리
    parts = url.rstrip('/').split('/')

    # URL 유효성 검사
    if 'universe.roboflow.com' not in url:
        print("❌ 올바른 Roboflow Universe URL이 아닙니다!")
        return None

    try:
        workspace = parts[3]
        project = parts[4]
        version = parts[5]

        print("✅ URL 분석 완료!")
        print(f"Workspace: {workspace}")
        print(f"Project: {project}")
        print(f"Version: {version}")
        print("\n다운로드 명령어:")
        print(f"python roboflow_integration.py \\")
        print(f"    --api-key YOUR_API_KEY \\")
        print(f"    download \\")
        print(f"    --workspace {workspace} \\")
        print(f"    --project {project} \\")
        print(f"    --version {version}")

        return {
            'workspace': workspace,
            'project': project,
            'version': version
        }
    except IndexError:
        print("❌ URL 형식이 올바르지 않습니다!")
        print("올바른 형식: https://universe.roboflow.com/workspace/project/version")
        return None

# 사용 예제
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Roboflow Universe URL을 입력하세요: ")

    extract_roboflow_info(url)
```

**사용 방법:**
```bash
python extract_url_info.py "https://universe.roboflow.com/joseph-nelson/bccd/2"
```

**출력:**
```
✅ URL 분석 완료!
Workspace: joseph-nelson
Project: bccd
Version: 2

다운로드 명령어:
python roboflow_integration.py \
    --api-key YOUR_API_KEY \
    download \
    --workspace joseph-nelson \
    --project bccd \
    --version 2
```

---

## 📚 실습 문제

다음 URL들에서 정보를 추출해보세요:

### 문제 1
```
https://universe.roboflow.com/my-team/cat-detector/3
```

<details>
<summary>정답 보기</summary>

```
workspace = "my-team"
project = "cat-detector"
version = 3
```
</details>

### 문제 2
```
https://universe.roboflow.com/university-project/face-mask-detection/1
```

<details>
<summary>정답 보기</summary>

```
workspace = "university-project"
project = "face-mask-detection"
version = 1
```
</details>

### 문제 3
```
https://universe.roboflow.com/roboflow-universe-projects/people-detection-o4rdr/5
```

<details>
<summary>정답 보기</summary>

```
workspace = "roboflow-universe-projects"
project = "people-detection-o4rdr"
version = 5
```
</details>

---

## 🔗 자주 묻는 질문 (FAQ)

### Q1: URL에 ?가 포함되어 있으면 어떻게 하나요?
```
https://universe.roboflow.com/my-workspace/my-project/1?tab=dataset
```

**A:** ? 이후는 무시하세요!
```
workspace = "my-workspace"
project = "my-project"
version = 1
```

### Q2: 자신의 workspace URL은 어떻게 다른가요?

Universe (공개):
```
https://universe.roboflow.com/workspace/project/version
```

자신의 workspace (비공개):
```
https://app.roboflow.com/workspace/project/version
```

둘 다 같은 방식으로 추출하면 됩니다!

### Q3: 버전이 여러 개인데 어떤 걸 써야 하나요?

보통 **가장 높은 버전 번호**가 최신 버전입니다.
예: 버전 1, 2, 3이 있다면 → 3을 사용

---

## ✅ 체크리스트

정보를 제대로 추출했는지 확인하세요:

- [ ] URL을 전체 복사했나요?
- [ ] 슬래시(/)로 구분된 부분을 정확히 찾았나요?
- [ ] workspace에 슬래시가 없나요?
- [ ] project에 슬래시가 없나요?
- [ ] version은 숫자인가요?
- [ ] 대소문자를 URL과 정확히 동일하게 썼나요?

모두 체크했다면 성공입니다! 🎉

---

**이제 URL만 보면 바로 정보를 추출할 수 있을 거예요!** 🚀
