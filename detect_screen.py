#!/usr/bin/env python3
"""
화면 캡처 + YOLO12 실시간 객체 감지
게임이나 다른 프로그램 화면에서 Rune을 실시간으로 감지합니다.
"""

import cv2
import numpy as np
import time
from mss import mss
from ultralytics import YOLO
import argparse


class ScreenDetector:
    """화면 캡처 및 실시간 객체 감지"""

    def __init__(self, model_path, conf_threshold=0.25, iou_threshold=0.45):
        """
        초기화

        Args:
            model_path: YOLO 모델 경로
            conf_threshold: 신뢰도 임계값
            iou_threshold: IoU 임계값
        """
        print(f"YOLO 모델 로딩 중: {model_path}")
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.sct = mss()

        print("✅ 모델 로딩 완료!")

    def get_screen_region(self):
        """
        캡처할 화면 영역 선택

        Returns:
            dict: 화면 영역 정보 {"top": y, "left": x, "width": w, "height": h}
        """
        print("\n" + "="*60)
        print("화면 영역 선택")
        print("="*60)
        print("\n사용 가능한 모니터:")

        for i, monitor in enumerate(self.sct.monitors):
            if i == 0:  # 전체 화면
                print(f"  0. 전체 화면 {monitor['width']}x{monitor['height']}")
            else:
                print(f"  {i}. 모니터 {i}: {monitor['width']}x{monitor['height']}")

        print(f"  {len(self.sct.monitors)}. 커스텀 영역")

        choice = input("\n선택 (0-{}): ".format(len(self.sct.monitors)))

        try:
            choice = int(choice)

            if 0 <= choice < len(self.sct.monitors):
                monitor = self.sct.monitors[choice]
                print(f"\n✅ 선택: 모니터 {choice} ({monitor['width']}x{monitor['height']})")
                return monitor
            elif choice == len(self.sct.monitors):
                # 커스텀 영역
                print("\n커스텀 영역 설정:")
                x = int(input("  X 좌표 (왼쪽): "))
                y = int(input("  Y 좌표 (위): "))
                w = int(input("  너비: "))
                h = int(input("  높이: "))

                region = {"top": y, "left": x, "width": w, "height": h}
                print(f"\n✅ 커스텀 영역 설정: {w}x{h} at ({x}, {y})")
                return region
            else:
                print("⚠️ 잘못된 선택. 전체 화면을 사용합니다.")
                return self.sct.monitors[0]
        except ValueError:
            print("⚠️ 잘못된 입력. 전체 화면을 사용합니다.")
            return self.sct.monitors[0]

    def capture_screen(self, region):
        """
        화면 캡처

        Args:
            region: 캡처할 영역

        Returns:
            numpy.ndarray: BGR 형식의 이미지
        """
        # 화면 캡처
        screenshot = self.sct.grab(region)

        # numpy 배열로 변환
        img = np.array(screenshot)

        # BGRA -> BGR 변환
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        return img

    def detect_and_draw(self, frame):
        """
        객체 감지 및 결과 그리기

        Args:
            frame: 입력 이미지

        Returns:
            numpy.ndarray: 감지 결과가 그려진 이미지
        """
        # YOLO 추론
        results = self.model.predict(
            source=frame,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            verbose=False
        )

        # 결과 이미지
        annotated_frame = results[0].plot()

        return annotated_frame, results[0]

    def run(self, region=None, show_fps=True, save_video=None):
        """
        실시간 화면 감지 시작

        Args:
            region: 캡처할 영역 (None이면 사용자에게 선택 받음)
            show_fps: FPS 표시 여부
            save_video: 비디오 저장 경로 (None이면 저장 안 함)
        """
        # 영역 선택
        if region is None:
            region = self.get_screen_region()

        print("\n" + "="*60)
        print("화면 감지 시작!")
        print("="*60)
        print("\n💡 조작 방법:")
        print("  - 'q': 종료")
        print("  - 'p': 일시정지/재개")
        print("  - 's': 스크린샷 저장")
        print("  - 'c': 신뢰도 임계값 변경")
        print("="*60 + "\n")

        # 비디오 저장 설정
        video_writer = None
        if save_video:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = 30
            width = region['width']
            height = region['height']
            video_writer = cv2.VideoWriter(save_video, fourcc, fps, (width, height))
            print(f"📹 비디오 저장 중: {save_video}")

        # FPS 계산용
        frame_count = 0
        start_time = time.time()
        fps = 0

        paused = False
        screenshot_count = 0

        try:
            while True:
                if not paused:
                    # 화면 캡처
                    frame = self.capture_screen(region)

                    # 객체 감지
                    annotated_frame, results = self.detect_and_draw(frame)

                    # FPS 계산
                    frame_count += 1
                    elapsed = time.time() - start_time
                    if elapsed > 0:
                        fps = frame_count / elapsed

                    # FPS 및 감지 수 표시
                    if show_fps:
                        info_text = f'FPS: {fps:.1f} | Detections: {len(results.boxes)}'
                        cv2.putText(annotated_frame, info_text,
                                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                   1, (0, 255, 0), 2)

                    # 화면 표시
                    cv2.imshow('Screen Rune Detection (Press Q to quit)', annotated_frame)

                    # 비디오 저장
                    if video_writer:
                        video_writer.write(annotated_frame)

                    # FPS 리셋 (1초마다)
                    if elapsed >= 1.0:
                        frame_count = 0
                        start_time = time.time()

                # 키 입력 처리
                key = cv2.waitKey(1) & 0xFF

                if key == ord('q'):
                    print("\n종료합니다...")
                    break
                elif key == ord('p'):
                    paused = not paused
                    status = "일시정지" if paused else "재개"
                    print(f"\n⏯️  {status}")
                elif key == ord('s'):
                    # 스크린샷 저장
                    screenshot_count += 1
                    filename = f"screenshot_{screenshot_count}.jpg"
                    cv2.imwrite(filename, annotated_frame)
                    print(f"\n📸 스크린샷 저장: {filename}")
                elif key == ord('c'):
                    # 신뢰도 임계값 변경
                    print(f"\n현재 신뢰도 임계값: {self.conf_threshold}")
                    try:
                        new_conf = float(input("새 신뢰도 임계값 (0.0-1.0): "))
                        if 0.0 <= new_conf <= 1.0:
                            self.conf_threshold = new_conf
                            print(f"✅ 신뢰도 임계값 변경: {new_conf}")
                        else:
                            print("⚠️ 0.0-1.0 사이의 값을 입력하세요.")
                    except ValueError:
                        print("⚠️ 잘못된 입력입니다.")

        except KeyboardInterrupt:
            print("\n\n종료합니다...")
        finally:
            # 정리
            if video_writer:
                video_writer.release()
                print(f"\n✅ 비디오 저장 완료: {save_video}")

            cv2.destroyAllWindows()

            print("\n" + "="*60)
            print("화면 감지 종료")
            print("="*60)


def main():
    parser = argparse.ArgumentParser(description='화면 캡처 + YOLO12 실시간 객체 감지')
    parser.add_argument('--model', type=str,
                       default='models/rune_detection/weights/best.pt',
                       help='YOLO 모델 경로 (기본: models/rune_detection/weights/best.pt)')
    parser.add_argument('--conf', type=float, default=0.25,
                       help='신뢰도 임계값 (기본: 0.25)')
    parser.add_argument('--iou', type=float, default=0.45,
                       help='IoU 임계값 (기본: 0.45)')
    parser.add_argument('--monitor', type=int, default=None,
                       help='모니터 번호 (0=전체, 1=첫 번째 모니터, ...)')
    parser.add_argument('--region', type=str, default=None,
                       help='커스텀 영역 "x,y,width,height" (예: "100,100,800,600")')
    parser.add_argument('--no-fps', action='store_true',
                       help='FPS 표시 안 함')
    parser.add_argument('--save', type=str, default=None,
                       help='비디오 저장 경로 (예: output/screen_recording.mp4)')

    args = parser.parse_args()

    # 감지기 초기화
    detector = ScreenDetector(
        model_path=args.model,
        conf_threshold=args.conf,
        iou_threshold=args.iou
    )

    # 영역 설정
    region = None
    if args.region:
        # 커스텀 영역 파싱
        try:
            x, y, w, h = map(int, args.region.split(','))
            region = {"top": y, "left": x, "width": w, "height": h}
            print(f"커스텀 영역: {w}x{h} at ({x}, {y})")
        except ValueError:
            print("⚠️ 잘못된 영역 형식. 대화형 선택으로 진행합니다.")
    elif args.monitor is not None:
        # 모니터 번호로 선택
        try:
            region = detector.sct.monitors[args.monitor]
            print(f"모니터 {args.monitor} 선택: {region['width']}x{region['height']}")
        except IndexError:
            print(f"⚠️ 모니터 {args.monitor}을(를) 찾을 수 없습니다. 대화형 선택으로 진행합니다.")

    # 실행
    detector.run(
        region=region,
        show_fps=not args.no_fps,
        save_video=args.save
    )


if __name__ == '__main__':
    main()
