import os
import argparse
from datetime import datetime

import cv2
from camera_utils import check_camera_idx
from process import LS_Detector
from notifier import send_notification_api


log_folder = "log"
os.makedirs(log_folder, exist_ok=True)


def export_log(msg, log_path, is_notified=False):
    now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    tm_msg = '{}\t{}'.format(now, msg)
    print(tm_msg)

    with open(log_path, "a") as f:
        f.write('{}\n'.format(tm_msg))
        
        if is_notified:
            ret = send_notification_api(tm_msg)
            f.write('{}\t{}\n'.format(now, ret))


def ls_detect(cap, is_show, log_file):
    # print("hello world!!!!")
    export_log("Started...", log_file, True)
    
    processor = LS_Detector()
    cur_signal = None
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0:
        fps = 25
        cap.set(cv2.CAP_PROP_FPS, fps)
    L_num = 0
    S_num = 0
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

                    if response_data["signal"] is None:
                        # logger.info("No changed.")
                        pass
                    else:
                        cur_signal = response_data["signal"]
                        if cur_signal == "L":
                            L_num += 1
                        else:
                            S_num += 1
                        export_log("TICKER:  Current Status: {}\tLs = {}\tSs = {}".format(cur_signal, L_num, S_num), log_file, True)
                if is_show:
                    cv2.imshow('frame', response_data["frame"])
            else:
                export_log("Failed to Process: {}".format(response_data['descript']), log_file)
                break
        else:
            export_log("Done process...", log_file, True)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def main(args):
    is_camera = args.camera
    video_file = args.video
    is_show = args.show

    log_file = args.log_file
    if log_file is None:
        log_file = datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + ".log"

    log_path = os.path.join(log_folder, log_file)

    if not is_camera and video_file is None:
        export_log("Invalid input argument...", log_file)
        return
    if is_camera:
        cam_idx = check_camera_idx()
        # cam_idx = [0]
        if cam_idx == []:
            export_log("\tThere is no available camera.", log_file)
            return
        elif len(cam_idx) != 1:
            export_log("There are several available cameras. Please select one of them.\nAvailable Camera indices: {}".format(cam_idx),
                       log_file)
            while True:
                idx = input("Please select camera: ")
                try:
                    idx = int(idx)
                    if idx in cam_idx:
                        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                        break
                    else:
                        print("Error: invalid camera index.")
                except ValueError:
                    export_log("This is invalid data type. Input integer number.", log_file)
        else:
            export_log("The connected camera index is {}".format(cam_idx[0]), log_file)
            cap = cv2.VideoCapture(cam_idx[0], cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(video_file)

    ls_detect(cap, is_show, log_path)


if __name__ == "__main__":

    # default="chart line light Right to Left.mov"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--camera", action="store_true", help="camera to be processed.")
    parser.add_argument("-v", "--video", type=str, help="Path for video file to be processed.")
    parser.add_argument("--show", action="store_true", help="Showing process and result frame.")
    parser.add_argument("--log_file", type=str, help="log file path")
    args = parser.parse_args()
    main(args)
