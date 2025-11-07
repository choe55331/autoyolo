# 64비트 Kiwoom Open API 테스트 가이드

이 디렉토리는 64비트 Python 환경에서 Kiwoom Open API를 사용하여 과거 분봉 데이터를 조회하는 테스트 스크립트를 포함합니다.

## 📋 필수 요구사항

### 1. Kiwoom 64비트 Open API 설치

1. **Visual C++ 재배포 패키지(x64) 설치**
   - [Microsoft Visual C++ 재배포 패키지](https://aka.ms/vs/17/release/vc_redist.x64.exe) 다운로드 및 설치

2. **64비트 Open API 다운로드**
   - GitHub: https://github.com/teranum/64bit-kiwoom-openapi
   - Release에서 최신 버전 다운로드

3. **설치 절차**
   ```
   1. 압축 해제
   2. KHOpenAPI64.ocx를 C:\OpenAPI\ 폴더에 복사
   3. 관리자 권한으로 명령 프롬프트 실행
   4. 다음 명령 실행:
      cd C:\OpenAPI
      regsvr32 KHOpenAPI64.ocx
   ```

### 2. Python 환경

- **Python 64비트** 버전 필수 (32비트 불가)
- Python 3.7 이상 권장

### 3. 필수 라이브러리 설치

```bash
pip install pywin32
```

## 🚀 사용 방법

### 기본 테스트 (test_64bit_openapi_debug.py)

이벤트 기반 방식으로 로그인 및 분봉 조회를 수행합니다.

```bash
python tests/manual/test_64bit_openapi_debug.py
```

**특징:**
- win32event를 사용한 이벤트 동기화
- 삼성전자(005930) 1분봉 100개 조회
- 상세한 디버깅 정보 출력

### 고급 테스트 (test_64bit_openapi_advanced.py) ⭐ 권장

메시지 펌프를 사용하여 더 안정적으로 작동합니다.

```bash
python tests/manual/test_64bit_openapi_advanced.py
```

**특징:**
- `pythoncom.PumpWaitingMessages()` 메시지 펌프 사용
- COM 오류 0x8000FFFF 해결
- 더 안정적인 이벤트 처리
- 타임아웃 설정 가능

**이 버전을 먼저 시도하세요!**

## 📊 분봉 데이터 조회

### 지원하는 틱 범위

- 1분봉: tick="1"
- 3분봉: tick="3"
- 5분봉: tick="5"
- 10분봉: tick="10"
- 15분봉: tick="15"
- 30분봉: tick="30"
- 45분봉: tick="45"
- 60분봉: tick="60"

### 코드 예제

```python
from test_64bit_openapi_advanced import Kiwoom64APIAdvanced
import pythoncom

# API 객체 생성
kiwoom = Kiwoom64APIAdvanced()

# ActiveX 생성
if kiwoom.create_ocx():
    # 로그인
    if kiwoom.connect(timeout=60):
        # 분봉 데이터 조회
        # 삼성전자 5분봉 200개
        result = kiwoom.get_minute_data("005930", "5", timeout=30)

        if result:
            print(f"조회된 데이터: {len(result['data'])}개")

            # 데이터 처리
            for row in result['data']:
                print(f"{row['체결시간']}: {row['현재가']}")

        # 연결 종료
        kiwoom.disconnect()
```

### CSV로 저장

```python
import pandas as pd

# 분봉 데이터 조회 후
if result:
    df = pd.DataFrame(result['data'])
    df.to_csv('samsung_5min.csv', index=False, encoding='utf-8-sig')
    print("CSV 저장 완료!")
```

## ❌ 문제 해결

### 1. COM 오류 0x8000FFFF

**증상:**
```
❌ COM 오류 발생:
   오류 코드: -2147418113 (0x8000FFFF)
   오류 메시지: 오류입니다.
```

**해결 방법:**
1. **메시지 펌프 사용** ⭐ 가장 효과적
   - `test_64bit_openapi_advanced.py` 사용
   - `pythoncom.PumpWaitingMessages()` 호출

2. **다른 Kiwoom 프로그램 종료**
   - 작업 관리자에서 모든 Kiwoom 관련 프로세스 종료

3. **재부팅**
   - Windows 재부팅 후 재시도

4. **OCX 재등록**
   ```bash
   # 관리자 권한 명령 프롬프트
   cd C:\OpenAPI
   regsvr32 /u KHOpenAPI64.ocx
   regsvr32 KHOpenAPI64.ocx
   ```

### 2. ActiveX 생성 실패

**증상:**
```
❌ ActiveX 컨트롤 생성 실패
```

**해결 방법:**
1. OCX 파일 존재 확인
   ```bash
   dir C:\OpenAPI\KHOpenAPI64.ocx
   ```

2. 레지스트리 확인
   ```bash
   reg query "HKEY_CLASSES_ROOT\KHOPENAPI.KHOpenAPICtrl.1"
   ```

3. OCX 재설치
   - 위의 설치 절차 다시 수행

### 3. 로그인 실패

**증상:**
```
❌ OnEventConnect: 로그인 실패 (오류코드: -100)
```

**해결 방법:**
1. **Kiwoom 계정 확인**
   - 영웅문 PC 버전에서 로그인 가능한지 확인
   - 모의투자/실거래 계정 확인

2. **서버 점검 시간**
   - 주말/공휴일: 서버 점검 중일 수 있음
   - 평일 정규 장 시간 (09:00-15:30) 또는 종료 후 시도

3. **방화벽 설정**
   - Windows 방화벽에서 Python 허용

### 4. TR 데이터 수신 실패

**증상:**
```
❌ 응답 시간 초과 (30초)
```

**해결 방법:**
1. **타임아웃 증가**
   ```python
   result = kiwoom.get_minute_data("005930", "1", timeout=60)
   ```

2. **종목코드 확인**
   - 6자리 종목코드 (예: "005930")
   - 앞에 0이 있는 경우 문자열로 입력

3. **조회 제한**
   - Kiwoom API는 초당 조회 횟수 제한 있음
   - 연속 조회 시 1초 대기 추가

### 5. Python 32비트 사용

**증상:**
```
파일을 찾을 수 없습니다
```

**해결 방법:**
- **Python 64비트 버전으로 재설치 필수**
- 확인 방법:
  ```python
  import sys
  print(sys.maxsize > 2**32)  # True면 64비트, False면 32비트
  ```

## 📝 오류 코드 참조

### 로그인 오류 코드
- `0`: 정상 처리
- `-100`: 사용자 정보 교환 실패
- `-101`: 서버 접속 실패
- `-102`: 버전 처리 실패

### TR 요청 오류 코드
- `0`: 정상 처리
- `-200`: 시세 과부하
- `-201`: 조회(TR) 횟수 초과

## 🔍 디버깅 팁

### 1. COM 초기화 확인

```python
import pythoncom
import sys

print(f"Python 버전: {sys.version}")
print(f"64비트: {sys.maxsize > 2**32}")

try:
    pythoncom.CoInitialize()
    print("COM 초기화 성공")
except Exception as e:
    print(f"COM 초기화 실패: {e}")
```

### 2. OCX 등록 확인

```python
import winreg

try:
    key = winreg.OpenKey(
        winreg.HKEY_CLASSES_ROOT,
        "KHOPENAPI.KHOpenAPICtrl.1\\CLSID"
    )
    clsid = winreg.QueryValue(key, None)
    print(f"CLSID: {clsid}")
    winreg.CloseKey(key)
except:
    print("OCX 미등록")
```

### 3. 상세 로그 출력

스크립트에 이미 상세한 로그가 포함되어 있습니다:
- 각 단계별 진행 상황
- 오류 발생 시 traceback
- COM 오류 코드 및 메시지

## 📚 참고 자료

- **64비트 Open API GitHub**: https://github.com/teranum/64bit-kiwoom-openapi
- **Kiwoom 공식 OpenAPI+**: https://www.kiwoom.com/
- **TR 문서**: opt10080 (주식분봉차트조회)

## 🎯 다음 단계

1. **자동화 스크립트 작성**
   - 여러 종목 일괄 조회
   - 데이터베이스 저장
   - 스케줄러 연동

2. **데이터 분석**
   - pandas로 데이터 분석
   - matplotlib으로 차트 그리기
   - 기술적 지표 계산

3. **실시간 데이터**
   - 실시간 시세 수신
   - 체결 알림
   - 자동 매매 (신중하게!)

## ⚠️ 주의사항

1. **과도한 조회 금지**
   - API 사용 제한 있음
   - 초당 5회 이하 권장

2. **개인정보 보호**
   - 계정 정보 절대 공유 금지
   - 로그 파일 관리 주의

3. **투자 판단**
   - 이 도구는 데이터 조회용
   - 투자 판단은 본인 책임

## 💡 도움이 필요하신가요?

문제가 계속되면:
1. 위의 문제 해결 섹션 참조
2. Kiwoom 고객센터 문의
3. GitHub Issue 등록

**성공적인 테스트를 기원합니다! 📈**
