"""
64비트 Kiwoom Open API 로그인 및 분봉 데이터 조회 테스트

이 스크립트는 64비트 Python 환경에서 Kiwoom Open API를 사용하여
로그인하고 과거 분봉 데이터를 조회합니다.

필수 요구사항:
1. C:\OpenAPI\KHOpenAPI64.ocx 설치
2. Visual C++ 재배포 패키지(x64) 설치
3. 관리자 권한으로 OCX 등록 완료
"""

import sys
import time
import win32com.client
import pythoncom
import win32event
import win32api


class Kiwoom64API:
    """64비트 Kiwoom Open API 클래스"""

    def __init__(self):
        self.ocx = None
        self.login_event = None
        self.tr_event = None
        self.connected = False
        self.tr_data = {}
        self.screen_no = "0101"

    def print_header(self, title, step=None):
        """헤더 출력"""
        print("\n" + "=" * 80)
        if step:
            print(f"  {step} {title}")
        else:
            print(f"  {title}")
        print("=" * 80 + "\n")

    def create_ocx(self):
        """ActiveX 컨트롤 생성"""
        self.print_header("ActiveX 컨트롤 생성", "1️⃣")

        try:
            # COM 초기화
            pythoncom.CoInitialize()
            print("✅ COM 초기화 성공")

            # ActiveX 컨트롤 생성
            self.ocx = win32com.client.DispatchWithEvents(
                "KHOPENAPI.KHOpenAPICtrl.1",
                KiwoomEventHandler
            )
            self.ocx.parent = self
            print("✅ ActiveX 컨트롤 생성 성공")

            # 이벤트 생성
            self.login_event = win32event.CreateEvent(None, 0, 0, None)
            self.tr_event = win32event.CreateEvent(None, 0, 0, None)
            print("✅ 이벤트 객체 생성 완료")

            return True

        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return False

    def connect(self):
        """로그인"""
        self.print_header("로그인 시도", "2️⃣")

        try:
            print("🔐 CommConnect() 호출...")
            print("   ⏳ 로그인 창이 나타나면 ID/PW를 입력해주세요")
            print("   ⏳ 자동 로그인 설정 시 자동으로 진행됩니다")

            # CommConnect 호출
            ret = self.ocx.CommConnect()
            print(f"   CommConnect 반환값: {ret}")

            if ret != 0:
                print(f"❌ CommConnect 실패: {ret}")
                return False

            # 로그인 대기 (최대 60초)
            print("   ⏳ 로그인 응답 대기 중...")
            result = win32event.WaitForSingleObject(self.login_event, 60000)

            if result == win32event.WAIT_TIMEOUT:
                print("❌ 로그인 시간 초과 (60초)")
                return False

            # 연결 상태 확인
            state = self.ocx.GetConnectState()
            print(f"   연결 상태: {state}")

            if state == 1:
                print("✅ 로그인 성공!")
                self.connected = True

                # 계정 정보 출력
                self.print_account_info()
                return True
            else:
                print("❌ 로그인 실패")
                return False

        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return False

    def print_account_info(self):
        """계정 정보 출력"""
        try:
            # 계정 목록
            accounts = self.ocx.GetLoginInfo("ACCNO")
            account_list = accounts.split(';') if accounts else []

            # 사용자 정보
            user_id = self.ocx.GetLoginInfo("USER_ID")
            user_name = self.ocx.GetLoginInfo("USER_NAME")

            print(f"\n📌 계정 정보:")
            print(f"   사용자 ID: {user_id}")
            print(f"   사용자명: {user_name}")
            print(f"   보유 계좌: {len(account_list)}개")
            for i, acc in enumerate(account_list, 1):
                if acc:
                    print(f"      {i}. {acc}")

        except Exception as e:
            print(f"⚠️  계정 정보 조회 오류: {e}")

    def get_minute_data(self, code, tick="1", count=100):
        """분봉 데이터 조회

        Args:
            code: 종목코드 (예: "005930")
            tick: 틱범위 (1분=1, 3분=3, 5분=5, 10분=10, 15분=15, 30분=30, 45분=45, 60분=60)
            count: 조회 개수 (최대 900)
        """
        self.print_header(f"분봉 데이터 조회 - {code} ({tick}분봉)", "3️⃣")

        if not self.connected:
            print("❌ 로그인이 필요합니다")
            return None

        try:
            # TR 요청 설정
            self.ocx.SetInputValue("종목코드", code)
            self.ocx.SetInputValue("틱범위", tick)
            self.ocx.SetInputValue("수정주가구분", "1")  # 1:수정주가 반영

            print(f"📊 요청 정보:")
            print(f"   종목코드: {code}")
            print(f"   틱범위: {tick}분")
            print(f"   요청 개수: {count}")

            # TR 요청
            print("\n🔄 TR 요청 중...")
            ret = self.ocx.CommRqData(
                "분봉조회",           # Request Name
                "opt10080",          # TR Code (주식분봉차트조회)
                0,                   # 연속조회 (0:초기조회)
                self.screen_no
            )

            if ret != 0:
                print(f"❌ CommRqData 실패: {ret}")
                return None

            # TR 응답 대기 (최대 30초)
            print("⏳ 응답 대기 중...")
            result = win32event.WaitForSingleObject(self.tr_event, 30000)

            if result == win32event.WAIT_TIMEOUT:
                print("❌ 응답 시간 초과 (30초)")
                return None

            # 결과 반환
            if self.tr_data:
                print(f"✅ 데이터 수신 완료: {len(self.tr_data.get('data', []))}개")
                return self.tr_data
            else:
                print("❌ 데이터 없음")
                return None

        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None

    def parse_tr_data(self, tr_code, rq_name):
        """TR 데이터 파싱"""
        try:
            data_count = self.ocx.GetRepeatCnt(tr_code, rq_name)
            print(f"\n📊 수신 데이터: {data_count}개")

            if data_count == 0:
                return

            # 데이터 저장
            self.tr_data = {
                'tr_code': tr_code,
                'rq_name': rq_name,
                'data': []
            }

            # 각 행 데이터 읽기
            for i in range(min(data_count, 10)):  # 처음 10개만 출력
                row = {
                    '체결시간': self.ocx.GetCommData(tr_code, rq_name, i, "체결시간").strip(),
                    '현재가': self.ocx.GetCommData(tr_code, rq_name, i, "현재가").strip(),
                    '시가': self.ocx.GetCommData(tr_code, rq_name, i, "시가").strip(),
                    '고가': self.ocx.GetCommData(tr_code, rq_name, i, "고가").strip(),
                    '저가': self.ocx.GetCommData(tr_code, rq_name, i, "저가").strip(),
                    '거래량': self.ocx.GetCommData(tr_code, rq_name, i, "거래량").strip(),
                }
                self.tr_data['data'].append(row)

                # 샘플 데이터 출력
                if i < 5:
                    print(f"\n   [{i+1}] {row['체결시간']}")
                    print(f"      시가: {row['시가']:>10} | 고가: {row['고가']:>10}")
                    print(f"      저가: {row['저가']:>10} | 종가: {row['현재가']:>10}")
                    print(f"      거래량: {row['거래량']:>10}")

            # 모든 데이터 저장
            for i in range(10, data_count):
                row = {
                    '체결시간': self.ocx.GetCommData(tr_code, rq_name, i, "체결시간").strip(),
                    '현재가': self.ocx.GetCommData(tr_code, rq_name, i, "현재가").strip(),
                    '시가': self.ocx.GetCommData(tr_code, rq_name, i, "시가").strip(),
                    '고가': self.ocx.GetCommData(tr_code, rq_name, i, "고가").strip(),
                    '저가': self.ocx.GetCommData(tr_code, rq_name, i, "저가").strip(),
                    '거래량': self.ocx.GetCommData(tr_code, rq_name, i, "거래량").strip(),
                }
                self.tr_data['data'].append(row)

        except Exception as e:
            print(f"⚠️  데이터 파싱 오류: {e}")
            import traceback
            traceback.print_exc()


class KiwoomEventHandler:
    """Kiwoom Open API 이벤트 핸들러"""

    def OnEventConnect(self, err_code):
        """로그인 이벤트"""
        if err_code == 0:
            print("\n✅ OnEventConnect: 로그인 성공")
        else:
            print(f"\n❌ OnEventConnect: 로그인 실패 (오류코드: {err_code})")

        # 이벤트 시그널
        if hasattr(self.parent, 'login_event'):
            win32event.SetEvent(self.parent.login_event)

    def OnReceiveTrData(self, screen_no, rq_name, tr_code, record_name, pre_next):
        """TR 데이터 수신 이벤트"""
        print(f"\n✅ OnReceiveTrData:")
        print(f"   화면번호: {screen_no}")
        print(f"   요청명: {rq_name}")
        print(f"   TR코드: {tr_code}")
        print(f"   레코드명: {record_name}")
        print(f"   연속조회키: {pre_next}")

        # 데이터 파싱
        self.parent.parse_tr_data(tr_code, rq_name)

        # 이벤트 시그널
        if hasattr(self.parent, 'tr_event'):
            win32event.SetEvent(self.parent.tr_event)

    def OnReceiveMsg(self, screen_no, rq_name, tr_code, msg):
        """메시지 수신 이벤트"""
        print(f"\n📩 메시지: {msg}")

    def OnReceiveChejanData(self, gubun, item_cnt, fid_list):
        """체결 데이터 수신 이벤트"""
        pass


def main():
    """메인 함수"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "              🚀 64비트 Open API 로그인 및 분봉 조회 테스트".center(86) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "  과거 분봉 데이터를 조회하여 출력합니다".center(82) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    # API 객체 생성
    kiwoom = Kiwoom64API()

    # ActiveX 생성
    if not kiwoom.create_ocx():
        print("\n❌ ActiveX 생성 실패")
        input("\n창을 닫으려면 Enter를 누르세요...")
        return

    # 로그인
    if not kiwoom.connect():
        print("\n❌ 로그인 실패")
        input("\n창을 닫으려면 Enter를 누르세요...")
        return

    # 분봉 데이터 조회
    # 삼성전자(005930) 1분봉 100개 조회
    result = kiwoom.get_minute_data("005930", "1", 100)

    if result:
        print("\n" + "=" * 80)
        print("  📊 최종 결과")
        print("=" * 80)
        print(f"\n✅ 총 {len(result.get('data', []))}개의 분봉 데이터 조회 완료")
        print(f"\n💾 데이터는 result 변수에 저장되었습니다")
        print(f"   result['data'][0] = {result['data'][0] if result.get('data') else 'None'}")
    else:
        print("\n❌ 분봉 데이터 조회 실패")

    # 종료
    print("\n" + "=" * 80)
    input("\n✅ 테스트 완료! 창을 닫으려면 Enter를 누르세요...")

    # COM 정리
    pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
