import cv2
from camera_utils import check_camera_idx
from process import LS_Detector


def ls_detect(cap, is_show):
    print("hello world!!!!")
    processor = LS_Detector()
    cur_signal = None
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0:
        fps = 25
        cap.set(cv2.CAP_PROP_FPS, fps)
    frame_count = 0
    while cap.isOpened():
        frame_count += 1
        ret, frame = cap.read()
        if frame_count % fps != 0:
            continue
        if ret:
            response_data = processor.infer(frame)
            if response_data["success"]:
                if cur_signal != response_data["signal"]:
                    cur_signal = response_data["signal"]
                    if cur_signal is None:
                        print(f"There is no signal. Please check again.")
                    else:
                        print(f"Current Status: {cur_signal}")
                if is_show:
                    cv2.imshow('frame', response_data["frame"])
            else:
                print(f"Failed to Process: {response_data['descript']}")
                break
        else:
            print("Done process...")
            break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def main(args):
    is_camera = args.camera
    video_file = args.video
    is_show = args.show

    if not is_camera and video_file is None:
        print("Invalid input argument...")
        return
    if is_camera:
        cam_idx = check_camera_idx()
        # cam_idx = [0]
        if cam_idx == []:
            print(f"\tThere is no available camera.")
            return
        elif len(cam_idx) != 1:
            print(f"There are several available cameras. Please select one of them.\nAvailable Camera indices: {cam_idx}")
            while True:
                idx = input("Please select camera: ")
                try:
                    idx = int(idx)
                    if idx in cam_idx:
                        cap = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)
                        break
                    else:
                        print("Please select available camera index...")
                except ValueError:
                    print("This is not a valid number. Try again.")
        else:
            print(f"The used camera index is {cam_idx[0]}")
            cap = cv2.VideoCapture(cam_idx[0], cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(video_file)

    ls_detect(cap, is_show)


if __name__ == "__main__":
    import argparse
    # default="chart line light Right to Left.mov"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--camera", action="store_true", help="camera to be processed.")
    parser.add_argument("-v", "--video", type=str, help="Path for video file to be processed.")
    parser.add_argument("--show", action="store_true", help="Showing process and result frame.")
    args = parser.parse_args()
    main(args)