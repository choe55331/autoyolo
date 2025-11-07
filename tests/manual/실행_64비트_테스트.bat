@echo off
chcp 65001 > nul
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                                                                       ║
echo ║           🚀 64비트 Kiwoom Open API 테스트 실행                       ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM 현재 디렉토리를 스크립트 위치로 변경
cd /d "%~dp0"

echo 📂 현재 위치: %CD%
echo.

REM Python 64비트 확인
echo ══════════════════════════════════════════════════════════════════════
echo  1️⃣ Python 환경 확인
echo ══════════════════════════════════════════════════════════════════════
echo.

python --version
if errorlevel 1 (
    echo.
    echo ❌ Python이 설치되어 있지 않습니다!
    echo    Python 64비트 버전을 설치해주세요.
    echo    다운로드: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

python -c "import sys; print('64비트:', sys.maxsize > 2**32)"
echo.

REM pywin32 설치 확인
echo ══════════════════════════════════════════════════════════════════════
echo  2️⃣ 필수 라이브러리 확인
echo ══════════════════════════════════════════════════════════════════════
echo.

python -c "import win32com.client" 2>nul
if errorlevel 1 (
    echo ⚠️  pywin32가 설치되어 있지 않습니다.
    echo    자동으로 설치를 시도합니다...
    echo.
    pip install pywin32
    echo.
) else (
    echo ✅ pywin32 설치됨
    echo.
)

REM OCX 확인
echo ══════════════════════════════════════════════════════════════════════
echo  3️⃣ Kiwoom OCX 확인
echo ══════════════════════════════════════════════════════════════════════
echo.

if exist "C:\OpenAPI\KHOpenAPI64.ocx" (
    echo ✅ KHOpenAPI64.ocx 파일 존재
    echo    경로: C:\OpenAPI\KHOpenAPI64.ocx
) else (
    echo ❌ KHOpenAPI64.ocx 파일이 없습니다!
    echo.
    echo    설치 방법:
    echo    1. https://github.com/teranum/64bit-kiwoom-openapi 에서 다운로드
    echo    2. KHOpenAPI64.ocx를 C:\OpenAPI\ 폴더에 복사
    echo    3. 관리자 권한 명령 프롬프트에서 실행:
    echo       cd C:\OpenAPI
    echo       regsvr32 KHOpenAPI64.ocx
    echo.
    pause
    exit /b 1
)
echo.

REM 테스트 선택
echo ══════════════════════════════════════════════════════════════════════
echo  4️⃣ 테스트 스크립트 선택
echo ══════════════════════════════════════════════════════════════════════
echo.
echo  [1] 기본 테스트 (이벤트 방식)
echo      - test_64bit_openapi_debug.py
echo      - win32event 사용
echo.
echo  [2] 고급 테스트 (메시지 펌프 방식) ⭐ 권장
echo      - test_64bit_openapi_advanced.py
echo      - COM 오류 0x8000FFFF 해결
echo      - 더 안정적
echo.
echo  [3] 종료
echo.

set /p choice="선택하세요 (1, 2, 3): "

if "%choice%"=="1" (
    echo.
    echo ══════════════════════════════════════════════════════════════════════
    echo  🚀 기본 테스트 실행
    echo ══════════════════════════════════════════════════════════════════════
    echo.
    python test_64bit_openapi_debug.py
) else if "%choice%"=="2" (
    echo.
    echo ══════════════════════════════════════════════════════════════════════
    echo  🚀 고급 테스트 실행 (권장)
    echo ══════════════════════════════════════════════════════════════════════
    echo.
    python test_64bit_openapi_advanced.py
) else if "%choice%"=="3" (
    echo.
    echo 👋 프로그램을 종료합니다.
    timeout /t 2 /nobreak > nul
    exit /b 0
) else (
    echo.
    echo ❌ 잘못된 선택입니다.
    pause
    exit /b 1
)

echo.
echo ══════════════════════════════════════════════════════════════════════
echo  ✅ 테스트 완료
echo ══════════════════════════════════════════════════════════════════════
echo.
pause
