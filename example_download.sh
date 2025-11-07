#!/bin/bash
# Roboflow 데이터셋 다운로드 예제 스크립트

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Roboflow 데이터셋 다운로드 예제 ===${NC}\n"

# API 키 확인
if [ -z "$ROBOFLOW_API_KEY" ]; then
    echo -e "${YELLOW}API 키가 설정되지 않았습니다.${NC}"
    echo "다음 중 하나를 선택하세요:"
    echo ""
    echo "1. 직접 입력:"
    echo "   export ROBOFLOW_API_KEY='your_api_key_here'"
    echo ""
    echo "2. .env 파일 생성:"
    echo "   echo 'ROBOFLOW_API_KEY=your_api_key_here' > .env"
    echo ""
    read -p "API 키를 입력하세요: " api_key
    export ROBOFLOW_API_KEY="$api_key"
fi

echo -e "${GREEN}사용 가능한 예제 데이터셋:${NC}\n"
echo "1. Playing Cards (카드 인식)"
echo "   - Workspace: augmented-startups"
echo "   - Project: playing-cards-ow27d"
echo "   - Version: 4"
echo ""
echo "2. Blood Cell Detection (혈구 감지)"
echo "   - Workspace: joseph-nelson"
echo "   - Project: bccd"
echo "   - Version: 2"
echo ""
echo "3. Vehicle Detection (차량 감지)"
echo "   - Workspace: roboflow-100"
echo "   - Project: vehicles-q0a2x"
echo "   - Version: 2"
echo ""
echo "4. 커스텀 (직접 입력)"
echo ""

read -p "선택하세요 (1-4): " choice

case $choice in
    1)
        workspace="augmented-startups"
        project="playing-cards-ow27d"
        version="4"
        output_dir="./data/playing-cards"
        ;;
    2)
        workspace="joseph-nelson"
        project="bccd"
        version="2"
        output_dir="./data/bccd"
        ;;
    3)
        workspace="roboflow-100"
        project="vehicles-q0a2x"
        version="2"
        output_dir="./data/vehicles"
        ;;
    4)
        read -p "Workspace: " workspace
        read -p "Project: " project
        read -p "Version: " version
        read -p "Output directory: " output_dir
        ;;
    *)
        echo "잘못된 선택입니다."
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}다운로드 시작...${NC}"
echo "Workspace: $workspace"
echo "Project: $project"
echo "Version: $version"
echo "Output: $output_dir"
echo ""

# 다운로드 실행
python roboflow_integration.py \
    --api-key "$ROBOFLOW_API_KEY" \
    download \
    --workspace "$workspace" \
    --project "$project" \
    --version "$version" \
    --location "$output_dir"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ 다운로드 완료!${NC}"
    echo ""
    echo "다음 단계:"
    echo "1. 데이터셋 확인: ls -la $output_dir"
    echo "2. config.yaml 수정:"
    echo "   dataset:"
    echo "     data_yaml: $output_dir/data.yaml"
    echo "3. 학습 시작: python train.py --data $output_dir/data.yaml"
else
    echo ""
    echo -e "${YELLOW}다운로드 실패${NC}"
    echo "문제 해결:"
    echo "1. API 키 확인"
    echo "2. 인터넷 연결 확인"
    echo "3. Workspace/Project/Version 이름 확인"
fi
