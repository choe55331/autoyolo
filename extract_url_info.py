#!/usr/bin/env python3
"""
Roboflow URL 정보 추출 도구
URL을 입력하면 workspace, project, version을 자동으로 추출합니다.
"""

import sys
import re


def extract_roboflow_info(url):
    """
    Roboflow URL에서 workspace, project, version 추출

    Args:
        url: Roboflow Universe 또는 App URL

    Returns:
        dict: workspace, project, version 정보 또는 None
    """
    # URL 정리 (끝의 슬래시와 쿼리 파라미터 제거)
    url = url.rstrip('/')
    url = url.split('?')[0]  # ? 이후 제거

    print(f"\n📋 분석 중인 URL: {url}\n")

    # URL 유효성 검사
    if 'universe.roboflow.com' not in url and 'app.roboflow.com' not in url:
        print("❌ 올바른 Roboflow URL이 아닙니다!")
        print("\n✅ 올바른 형식:")
        print("   - Universe: https://universe.roboflow.com/workspace/project/version")
        print("   - App: https://app.roboflow.com/workspace/project/version")
        return None

    # URL을 /로 분리
    parts = url.split('/')

    try:
        # 패턴: https://domain.com/workspace/project/version
        workspace = parts[3]
        project = parts[4]
        version = parts[5]

        # 버전이 숫자인지 확인
        try:
            version_num = int(version)
        except ValueError:
            print(f"⚠️  경고: 버전 '{version}'이 숫자가 아닙니다. 그대로 사용합니다.")
            version_num = version

        print("="*60)
        print("✅ URL 분석 완료!")
        print("="*60)
        print(f"📦 Workspace: {workspace}")
        print(f"📂 Project:   {project}")
        print(f"🔢 Version:   {version}")
        print("="*60)

        print("\n📥 다운로드 명령어:")
        print("-" * 60)
        print(f"python roboflow_integration.py \\")
        print(f"    --api-key YOUR_API_KEY \\")
        print(f"    download \\")
        print(f"    --workspace {workspace} \\")
        print(f"    --project {project} \\")
        print(f"    --version {version}")
        print("-" * 60)

        print("\n💡 간단한 버전 (API 키를 환경변수로 설정한 경우):")
        print("-" * 60)
        print(f"python roboflow_integration.py --api-key $ROBOFLOW_API_KEY \\")
        print(f"    download --workspace {workspace} --project {project} --version {version}")
        print("-" * 60)

        print("\n📝 복사용 (한 줄):")
        print("-" * 60)
        cmd = f"python roboflow_integration.py --api-key YOUR_API_KEY download --workspace {workspace} --project {project} --version {version}"
        print(cmd)
        print("-" * 60)

        return {
            'workspace': workspace,
            'project': project,
            'version': version
        }

    except IndexError:
        print("❌ URL 형식이 올바르지 않습니다!")
        print("\n올바른 형식:")
        print("   https://universe.roboflow.com/[workspace]/[project]/[version]")
        print("\n예제:")
        print("   https://universe.roboflow.com/joseph-nelson/bccd/2")
        return None


def interactive_mode():
    """대화형 모드"""
    print("="*60)
    print("🔍 Roboflow URL 정보 추출기")
    print("="*60)
    print("\nRoboflow Universe에서 데이터셋 URL을 복사해서 붙여넣으세요.")
    print("예: https://universe.roboflow.com/joseph-nelson/bccd/2")
    print("\n종료하려면 'quit' 또는 'exit'를 입력하세요.")
    print("="*60)

    while True:
        try:
            url = input("\n🔗 URL 입력: ").strip()

            if url.lower() in ['quit', 'exit', 'q']:
                print("\n👋 종료합니다.")
                break

            if not url:
                print("⚠️  URL을 입력해주세요.")
                continue

            result = extract_roboflow_info(url)

            if result:
                print("\n✨ 정보가 성공적으로 추출되었습니다!")

                # 다시 할지 물어보기
                again = input("\n다른 URL을 분석하시겠습니까? (y/n): ").strip().lower()
                if again not in ['y', 'yes', '']:
                    print("\n👋 종료합니다.")
                    break
            else:
                print("\n다시 시도해주세요.")

        except KeyboardInterrupt:
            print("\n\n👋 종료합니다.")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")


def main():
    """메인 함수"""
    if len(sys.argv) > 1:
        # 명령줄 인자가 있으면 해당 URL 분석
        url = sys.argv[1]
        extract_roboflow_info(url)
    else:
        # 명령줄 인자가 없으면 대화형 모드
        interactive_mode()


if __name__ == "__main__":
    main()
