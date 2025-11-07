@echo off
chcp 65001 >nul
echo ================================================================================
echo 🎮 화면 Rune 감지 - 실시간 화면 캡처
echo ================================================================================
echo.

REM 모델 파일 확인
if not exist "models\rune_detection\weights\best.pt" (
    echo ❌ 오류: 학습된 모델을 찾을 수 없어요!
    echo.
    echo 먼저 모델을 학습하세요:
    echo    학습_시작.bat
    echo.
    echo 또는 학습된 모델을 다운로드하세요.
    echo.
    pause
    exit /b 1
)

echo ✅ 학습된 모델 확인 완료!
echo.

REM mss 라이브러리 확인
python -c "import mss" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  화면 캡처 라이브러리가 설치되지 않았어요.
    echo.
    echo 자동으로 설치할까요?
    set /p install="설치하시겠습니까? (Y/n): "

    if /i "%install%"=="n" (
        echo 설치를 취소했습니다.
        pause
        exit /b 1
    )

    echo.
    echo 📦 mss 라이브러리 설치 중...
    pip install mss>=9.0.0

    if %errorlevel% neq 0 (
        echo.
        echo ❌ 설치 실패!
        echo 수동으로 설치하세요: pip install mss
        pause
        exit /b 1
    )

    echo ✅ 설치 완료!
    echo.
)

echo ================================================================================
echo 실행 모드 선택
echo ================================================================================
echo.
echo 1. 대화형 모드 (화면 영역 선택)
echo 2. 전체 화면 감지
echo 3. 첫 번째 모니터만 감지
echo 4. 커스텀 영역 (좌표 입력)
echo 5. 비디오 녹화 모드
echo.

set /p mode="선택 (1-5): "

if "%mode%"=="1" (
    echo.
    echo 📺 대화형 모드로 실행합니다...
    python detect_screen.py

) else if "%mode%"=="2" (
    echo.
    echo 📺 전체 화면 감지를 시작합니다...
    python detect_screen.py --monitor 0

) else if "%mode%"=="3" (
    echo.
    echo 📺 첫 번째 모니터 감지를 시작합니다...
    python detect_screen.py --monitor 1

) else if "%mode%"=="4" (
    echo.
    echo 커스텀 영역 설정:
    set /p x="X 좌표 (왼쪽): "
    set /p y="Y 좌표 (위): "
    set /p w="너비: "
    set /p h="높이: "

    echo.
    echo 📺 커스텀 영역 감지를 시작합니다...
    python detect_screen.py --region "%x%,%y%,%w%,%h%"

) else if "%mode%"=="5" (
    echo.
    echo 📹 비디오 녹화 모드
    set /p filename="저장할 파일 이름 (예: recording.mp4): "

    if "%filename%"=="" (
        set filename=screen_recording.mp4
    )

    echo.
    echo 📺 비디오를 녹화하며 감지를 시작합니다...
    echo 저장 위치: output\%filename%
    python detect_screen.py --save "output\%filename%"

) else (
    echo ❌ 잘못된 선택입니다.
    pause
    exit /b 1
)

if %errorlevel% equ 0 (
    echo.
    echo ================================================================================
    echo ✅ 화면 감지 종료
    echo ================================================================================
) else (
    echo.
    echo ================================================================================
    echo ⚠️ 오류가 발생했습니다
    echo ================================================================================
    echo.
    echo 문제 해결:
    echo   1. 모델 파일이 있는지 확인: models\rune_detection\weights\best.pt
    echo   2. 라이브러리 설치: pip install mss
    echo   3. 다른 프로그램이 화면을 사용 중인지 확인
)

echo.
pause
