@echo off
chcp 65001 >nul
echo ================================================================================
echo 🚀 YOLO12 Rune Detection - 학습 시작
echo ================================================================================
echo.

REM 데이터셋 경로 확인
if not exist "data\maple-rune-gloxg\data.yaml" (
    echo ❌ 오류: 데이터셋을 찾을 수 없어요!
    echo.
    echo 먼저 데이터셋을 다운로드하세요:
    echo    python easy_download.py "https://universe.roboflow.com/proyecto-kegnn/maple-rune-gloxg/dataset/5"
    echo.
    pause
    exit /b 1
)

echo ✅ 데이터셋 확인 완료!
echo.
echo 학습 옵션을 선택하세요:
echo.
echo 1. 빠른 테스트 (10 에포크, 약 10-20분)
echo 2. 기본 학습 (50 에포크, 약 1-2시간)
echo 3. 긴 학습 (100 에포크, 약 2-4시간)
echo 4. 커스텀 설정
echo.

set /p choice="선택 (1-4): "

if "%choice%"=="1" (
    set epochs=10
    echo.
    echo 📝 10 에포크로 빠른 테스트를 시작합니다...
) else if "%choice%"=="2" (
    set epochs=50
    echo.
    echo 📝 50 에포크로 기본 학습을 시작합니다...
) else if "%choice%"=="3" (
    set epochs=100
    echo.
    echo 📝 100 에포크로 긴 학습을 시작합니다...
) else if "%choice%"=="4" (
    set /p epochs="에포크 수를 입력하세요: "
    echo.
    echo 📝 %epochs% 에포크로 학습을 시작합니다...
) else (
    echo ❌ 잘못된 선택입니다.
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo 학습 시작!
echo ================================================================================
echo.
echo 💡 팁:
echo    - 학습 중에도 다른 작업을 할 수 있어요
echo    - 종료하려면 Ctrl+C를 누르세요
echo    - 학습 결과는 models/rune_detection 폴더에 저장됩니다
echo.
echo ================================================================================
echo.

python train.py --data data/maple-rune-gloxg/data.yaml --epochs %epochs%

if %errorlevel% equ 0 (
    echo.
    echo ================================================================================
    echo 🎉 학습 완료!
    echo ================================================================================
    echo.
    echo 학습된 모델: models\rune_detection\weights\best.pt
    echo.
    echo 이제 테스트해보세요:
    echo    python detect_rune.py --source test.jpg --model models\rune_detection\weights\best.pt
    echo.
) else (
    echo.
    echo ================================================================================
    echo ❌ 학습 중 오류가 발생했어요!
    echo ================================================================================
    echo.
    echo 문제 해결:
    echo    1. CPU_학습_가이드.md 파일을 확인하세요
    echo    2. config.yaml에서 device: cpu로 설정되어 있는지 확인하세요
    echo    3. 메모리 부족이면 배치 크기를 줄여보세요:
    echo       python train.py --data data/maple-rune-gloxg/data.yaml --epochs 10 --batch 4
    echo.
)

pause
