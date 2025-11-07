#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Roboflow 데이터셋 원클릭 다운로드 도구
URL만 붙여넣으면 끝! 초보자도 쉽게 사용 가능합니다.
"""

import os
import sys
import re


def print_header():
    """예쁜 헤더 출력"""
    print("\n" + "="*70)
    print("🎯 Roboflow 데이터셋 다운로드 도구 (초간단 버전)")
    print("="*70)


def print_step(step_num, message):
    """단계별 안내"""
    print(f"\n{'='*70}")
    print(f"📍 STEP {step_num}: {message}")
    print("="*70)


def extract_info_from_url(url):
    """
    URL에서 정보 추출 (더 똑똑한 버전)
    다양한 Roboflow URL 형식 지원
    """
    # URL 정리
    url = url.strip().rstrip('/')
    url = url.split('?')[0]  # 쿼리 파라미터 제거

    print(f"\n🔍 분석 중: {url}")

    # Roboflow URL인지 확인
    if 'roboflow.com' not in url:
        print("\n❌ 이건 Roboflow URL이 아닌 것 같아요!")
        print("   올바른 예시: https://universe.roboflow.com/workspace/project/version")
        return None

    # URL을 /로 분리
    parts = url.split('/')

    try:
        # 기본 패턴: .../workspace/project/version
        # 또는: .../workspace/project/dataset/version

        if 'dataset' in parts:
            # .../workspace/project/dataset/version 형식
            dataset_idx = parts.index('dataset')
            workspace = parts[dataset_idx - 2]
            project = parts[dataset_idx - 1]
            version = parts[dataset_idx + 1] if len(parts) > dataset_idx + 1 else '1'
        else:
            # .../workspace/project/version 형식
            workspace = parts[3]
            project = parts[4]
            version = parts[5] if len(parts) > 5 else '1'

        # 버전을 숫자로 변환 시도
        try:
            version = int(version)
        except:
            pass

        print("\n✅ URL 분석 완료!")
        print(f"   📦 작업공간(Workspace): {workspace}")
        print(f"   📂 프로젝트(Project): {project}")
        print(f"   🔢 버전(Version): {version}")

        return {
            'workspace': workspace,
            'project': project,
            'version': version
        }

    except Exception as e:
        print(f"\n❌ URL을 분석할 수 없어요: {e}")
        print("   URL을 다시 확인해주세요!")
        return None


def get_api_key():
    """API 키 받기 (친절한 버전)"""
    print("\n💡 API 키가 필요해요!")
    print("   API 키를 받는 방법:")
    print("   1️⃣  https://roboflow.com 접속")
    print("   2️⃣  로그인 (무료 회원가입 가능)")
    print("   3️⃣  우측 상단 프로필 클릭 → Settings")
    print("   4️⃣  좌측 메뉴 'Roboflow API' 클릭")
    print("   5️⃣  'Private API Key' 복사")

    # 환경변수에서 먼저 확인
    api_key = os.getenv('ROBOFLOW_API_KEY')
    if api_key:
        print(f"\n✅ 환경변수에서 API 키를 찾았어요! (키: {api_key[:10]}...)")
        use_env = input("   이 키를 사용할까요? (엔터/y = 예, n = 아니오): ").strip().lower()
        if use_env in ['', 'y', 'yes', 'ㅇ', '예']:
            return api_key

    # 직접 입력
    while True:
        api_key = input("\n🔑 API 키를 입력하세요 (또는 'skip'으로 건너뛰기): ").strip()

        if api_key.lower() == 'skip':
            print("\n⚠️  API 키 없이는 다운로드할 수 없어요!")
            print("   나중에 다시 실행해주세요.")
            return None

        if len(api_key) > 10:  # 최소한의 검증
            print(f"✅ API 키 입력 완료! (키: {api_key[:10]}...)")
            return api_key
        else:
            print("❌ API 키가 너무 짧아요. 다시 입력해주세요.")


def download_dataset(workspace, project, version, api_key):
    """데이터셋 다운로드"""
    from roboflow import Roboflow

    print("\n📥 다운로드를 시작합니다...")
    print(f"   작업공간: {workspace}")
    print(f"   프로젝트: {project}")
    print(f"   버전: {version}")

    # 저장 위치
    save_location = f"./data/{project}"
    print(f"   저장 위치: {save_location}")

    try:
        # Roboflow 클라이언트 초기화
        print("\n🔄 Roboflow에 연결 중...")
        rf = Roboflow(api_key=api_key)

        # 프로젝트 가져오기
        print("🔄 프로젝트 정보 가져오는 중...")
        project_obj = rf.workspace(workspace).project(project)

        # 버전 선택
        print(f"🔄 버전 {version} 선택 중...")
        dataset = project_obj.version(version)

        # 다운로드
        print("🔄 데이터셋 다운로드 중... (시간이 좀 걸릴 수 있어요)")
        dataset_path = dataset.download("yolov8", location=save_location)

        print("\n" + "="*70)
        print("🎉 다운로드 완료!")
        print("="*70)
        print(f"📁 저장 위치: {dataset_path}")

        # 다음 단계 안내
        print("\n" + "="*70)
        print("📚 다음 단계:")
        print("="*70)
        print(f"1️⃣  데이터셋 확인:")
        print(f"   ls -la {dataset_path}")
        print(f"\n2️⃣  config.yaml 파일 수정:")
        print(f"   dataset:")
        print(f"     data_yaml: {dataset_path}/data.yaml")
        print(f"\n3️⃣  모델 학습 시작:")
        print(f"   python train.py --data {dataset_path}/data.yaml --epochs 50")
        print(f"\n4️⃣  학습 완료 후 테스트:")
        print(f"   python detect_rune.py --source 이미지파일.jpg --model models/rune_detection/weights/best.pt")
        print("="*70)

        return dataset_path

    except Exception as e:
        print("\n❌ 다운로드 실패!")
        print(f"   오류: {e}")
        print("\n🔧 문제 해결 방법:")
        print("   1. API 키가 올바른지 확인")
        print("   2. 인터넷 연결 확인")
        print("   3. 작업공간/프로젝트/버전 이름 확인")
        print("   4. 해당 데이터셋에 접근 권한이 있는지 확인")
        return None


def main():
    """메인 함수"""
    print_header()

    # STEP 1: URL 입력
    print_step(1, "Roboflow Universe URL 입력")
    print("\n💡 Roboflow Universe에서 원하는 데이터셋을 찾으세요:")
    print("   1. https://universe.roboflow.com 접속")
    print("   2. 검색창에서 원하는 데이터셋 검색 (예: 'rune', 'playing cards')")
    print("   3. 마음에 드는 데이터셋 클릭")
    print("   4. 브라우저 주소창의 URL 전체를 복사")

    if len(sys.argv) > 1:
        # 명령줄에서 URL 제공
        url = sys.argv[1]
        print(f"\n입력된 URL: {url}")
    else:
        # 사용자에게 URL 입력 받기
        print("\n" + "-"*70)
        url = input("🔗 URL을 붙여넣으세요: ").strip()

    if not url:
        print("\n❌ URL을 입력하지 않았어요. 프로그램을 종료합니다.")
        return

    # STEP 2: URL 분석
    print_step(2, "URL 분석")
    info = extract_info_from_url(url)

    if not info:
        print("\n프로그램을 종료합니다.")
        return

    # STEP 3: API 키 받기
    print_step(3, "API 키 설정")
    api_key = get_api_key()

    if not api_key:
        return

    # STEP 4: 다운로드
    print_step(4, "데이터셋 다운로드")
    confirm = input("\n다운로드를 시작할까요? (엔터/y = 예, n = 아니오): ").strip().lower()

    if confirm in ['', 'y', 'yes', 'ㅇ', '예']:
        dataset_path = download_dataset(
            info['workspace'],
            info['project'],
            info['version'],
            api_key
        )

        if dataset_path:
            print("\n✨ 모든 작업이 완료되었어요! 이제 학습을 시작할 수 있어요! ✨")
    else:
        print("\n취소되었습니다.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        print("   문제가 계속되면 관리자에게 문의하세요.")
