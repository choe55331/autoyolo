"""
64비트 Kiwoom Open API 고급 테스트 (메시지 펌프 포함)

이 스크립트는 메시지 펌프를 사용하여 더 안정적으로 작동합니다.
COM 오류(0x8000FFFF)를 해결하기 위한 여러 기법을 포함합니다.

필수 요구사항:
1. C:\OpenAPI\KHOpenAPI64.ocx 설치
2. Visual C++ 재배포 패키지(x64) 설치
3. 관리자 권한으로 OCX 등록 완료
"""

import sys
import time
import win32com.client
import pythoncom
import pywintypes


class Kiwoom64APIAdvanced:
    """64비트 Kiwoom Open API 고급 클래스 (메시지 펌프 사용)"""

    def __init__(self):
        self.ocx = None
        self.connected = False
        self.login_err_code = None
        self.tr_data = {}
        self.tr_received = False
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
            # COM 초기화 (COINIT_MULTITHREADED 대신 APARTMENTTHREADED 사용)
            try:
                pythoncom.CoInitialize()
                print("✅ COM 초기화 성공 (APARTMENTTHREADED)")
            except:
                pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
                print("✅ COM 초기화 성공 (CoInitializeEx)")

            # ActiveX 컨트롤 생성
            print("\n🔄 ActiveX 컨트롤 생성 시도...")
            self.ocx = win32com.client.DispatchWithEvents(
                "KHOPENAPI.KHOpenAPICtrl.1",
                KiwoomEventHandlerAdvanced
            )
            self.ocx.parent = self
            print("✅ ActiveX 컨트롤 생성 성공")

            # 연결 상태 확인 (오류 무시)
            try:
                state = self.ocx.GetConnectState()
                print(f"   현재 연결 상태: {state} (0=미연결, 1=연결)")
            except Exception as e:
                print(f"   ⚠️  연결 상태 확인 실패 (무시): {e}")

            return True

        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            print(f"   오류 타입: {type(e).__name__}")

            if isinstance(e, pywintypes.com_error):
                print(f"   COM 오류 코드: {hex(e.hresult if hasattr(e, 'hresult') else 0)}")

            import traceback
            traceback.print_exc()
            return False

    def connect(self, timeout=60):
        """로그인 with 메시지 펌프

        Args:
            timeout: 타임아웃 (초)
        """
        self.print_header("로그인 시도 (메시지 펌프 사용)", "2️⃣")

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

            # 메시지 펌프를 사용하여 대기
            print("\n⏳ 로그인 응답 대기 중 (메시지 펌프 동작)...")
            start_time = time.time()

            while self.login_err_code is None:
                # 메시지 펌프
                pythoncom.PumpWaitingMessages()
                time.sleep(0.05)  # 50ms 대기

                # 타임아웃 체크
                if time.time() - start_time > timeout:
                    print(f"❌ 로그인 시간 초과 ({timeout}초)")
                    return False

                # 진행 상황 표시 (5초마다)
                elapsed = int(time.time() - start_time)
                if elapsed > 0 and elapsed % 5 == 0:
                    print(f"   ... {elapsed}초 경과 (최대 {timeout}초)")
                    time.sleep(1)  # 중복 출력 방지

            # 로그인 결과 확인
            if self.login_err_code == 0:
                print("\n✅ 로그인 성공!")
                self.connected = True

                # 연결 상태 재확인
                try:
                    state = self.ocx.GetConnectState()
                    print(f"   연결 상태: {state}")
                except:
                    pass

                # 계정 정보 출력
                self.print_account_info()
                return True
            else:
                print(f"\n❌ 로그인 실패 (오류코드: {self.login_err_code})")
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

    def get_minute_data(self, code, tick="1", timeout=30):
        """분봉 데이터 조회 with 메시지 펌프

        Args:
            code: 종목코드 (예: "005930")
            tick: 틱범위 (1분=1, 3분=3, 5분=5, 10분=10, 15분=15, 30분=30, 45분=45, 60분=60)
            timeout: 타임아웃 (초)
        """
        self.print_header(f"분봉 데이터 조회 - {code} ({tick}분봉)", "3️⃣")

        if not self.connected:
            print("❌ 로그인이 필요합니다")
            return None

        try:
            # 초기화
            self.tr_data = {}
            self.tr_received = False

            # TR 요청 설정
            self.ocx.SetInputValue("종목코드", code)
            self.ocx.SetInputValue("틱범위", tick)
            self.ocx.SetInputValue("수정주가구분", "1")  # 1:수정주가 반영

            print(f"📊 요청 정보:")
            print(f"   종목코드: {code}")
            print(f"   틱범위: {tick}분")

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
                print("   오류 코드 설명:")
                print("   -200: 시세과부하")
                print("   -201: 조회(TR)횟수 초과")
                return None

            # 메시지 펌프를 사용하여 대기
            print("⏳ 응답 대기 중 (메시지 펌프 동작)...")
            start_time = time.time()

            while not self.tr_received:
                # 메시지 펌프
                pythoncom.PumpWaitingMessages()
                time.sleep(0.05)  # 50ms 대기

                # 타임아웃 체크
                if time.time() - start_time > timeout:
                    print(f"❌ 응답 시간 초과 ({timeout}초)")
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
            for i in range(data_count):
                row = {
                    '체결시간': self.ocx.GetCommData(tr_code, rq_name, i, "체결시간").strip(),
                    '현재가': self.ocx.GetCommData(tr_code, rq_name, i, "현재가").strip(),
                    '시가': self.ocx.GetCommData(tr_code, rq_name, i, "시가").strip(),
                    '고가': self.ocx.GetCommData(tr_code, rq_name, i, "고가").strip(),
                    '저가': self.ocx.GetCommData(tr_code, rq_name, i, "저가").strip(),
                    '거래량': self.ocx.GetCommData(tr_code, rq_name, i, "거래량").strip(),
                }
                self.tr_data['data'].append(row)

                # 샘플 데이터 출력 (처음 5개)
                if i < 5:
                    print(f"\n   [{i+1}] {row['체결시간']}")
                    print(f"      시가: {row['시가']:>10} | 고가: {row['고가']:>10}")
                    print(f"      저가: {row['저가']:>10} | 종가: {row['현재가']:>10}")
                    print(f"      거래량: {row['거래량']:>10}")

            if data_count > 5:
                print(f"\n   ... 외 {data_count - 5}개 데이터")

        except Exception as e:
            print(f"⚠️  데이터 파싱 오류: {e}")
            import traceback
            traceback.print_exc()

    def disconnect(self):
        """연결 종료"""
        try:
            if self.ocx and self.connected:
                self.ocx.CommTerminate()
                print("✅ 연결 종료")
        except:
            pass

        try:
            pythoncom.CoUninitialize()
            print("✅ COM 정리 완료")
        except:
            pass


class KiwoomEventHandlerAdvanced:
    """Kiwoom Open API 이벤트 핸들러 (고급)"""

    def OnEventConnect(self, err_code):
        """로그인 이벤트"""
        if err_code == 0:
            print("\n✅ OnEventConnect: 로그인 성공")
        else:
            print(f"\n❌ OnEventConnect: 로그인 실패 (오류코드: {err_code})")
            print(self._get_error_message(err_code))

        # 오류 코드 저장
        self.parent.login_err_code = err_code

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

        # 수신 완료 플래그
        self.parent.tr_received = True

    def OnReceiveMsg(self, screen_no, rq_name, tr_code, msg):
        """메시지 수신 이벤트"""
        if msg:
            print(f"\n📩 메시지: {msg}")

    def OnReceiveChejanData(self, gubun, item_cnt, fid_list):
        """체결 데이터 수신 이벤트"""
        pass

    def _get_error_message(self, err_code):
        """오류 메시지 반환"""
        error_messages = {
            0: "정상처리",
            -100: "사용자 정보 교환 실패",
            -101: "서버 접속 실패",
            -102: "버전 처리 실패",
        }
        return f"   {error_messages.get(err_code, '알 수 없는 오류')}"


def main():
    """메인 함수"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "      🚀 64비트 Open API 고급 테스트 (메시지 펌프 사용)".center(86) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "  더 안정적인 로그인 및 과거 분봉 데이터 조회".center(82) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    # API 객체 생성
    kiwoom = Kiwoom64APIAdvanced()

    try:
        # ActiveX 생성
        if not kiwoom.create_ocx():
            print("\n❌ ActiveX 생성 실패")
            return

        # 로그인 (60초 타임아웃)
        if not kiwoom.connect(timeout=60):
            print("\n❌ 로그인 실패")
            return

        # 분봉 데이터 조회
        print("\n" + "=" * 80)
        print("  📊 데이터 조회 시작")
        print("=" * 80)

        # 삼성전자(005930) 1분봉 조회
        result = kiwoom.get_minute_data("005930", "1", timeout=30)

        if result:
            print("\n" + "=" * 80)
            print("  ✅ 최종 결과")
            print("=" * 80)
            print(f"\n✅ 총 {len(result.get('data', []))}개의 분봉 데이터 조회 완료")
            print(f"\n💾 데이터는 result 변수에 저장되었습니다")

            # 데이터 샘플 출력
            if result.get('data'):
                print(f"\n📌 첫 번째 데이터:")
                first_data = result['data'][0]
                for key, value in first_data.items():
                    print(f"   {key}: {value}")

                # CSV 저장 옵션
                print(f"\n💡 CSV 저장 예제:")
                print(f"   import pandas as pd")
                print(f"   df = pd.DataFrame(result['data'])")
                print(f"   df.to_csv('samsung_1min.csv', index=False, encoding='utf-8-sig')")
        else:
            print("\n❌ 분봉 데이터 조회 실패")

    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다")

    except Exception as e:
        print(f"\n❌ 예외 발생: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # 종료
        print("\n" + "=" * 80)
        print("  🔚 프로그램 종료")
        print("=" * 80)
        kiwoom.disconnect()
        input("\n✅ 테스트 완료! 창을 닫으려면 Enter를 누르세요...")


if __name__ == "__main__":
    main()
