import os
import argparse
from datetime import datetime
import time

import cv2
from camera_utils import check_camera_idx
from process import LS_Detector
from notifier import send_notification_api
from rect_input import GETRect
from capture import ScreenCap


log_folder = "log"
os.makedirs(log_folder, exist_ok=True)


def export_log(msg, ticker_name, log_path, is_notified=False):
    now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    tm_msg = '{}\t{}\t{}'.format(ticker_name, now, msg)
    print(tm_msg)

    with open(log_path, "a") as f:
        f.write('{}\n'.format(tm_msg))
        
        if is_notified:
            ret = send_notification_api(tm_msg)
            f.write('{}\t{}\t{}\n'.format(ticker_name, now, ret))


def ls_detect(cap, is_show, log_file, ticker_name = None):
    # print("hello world!!!!")
    if ticker_name is None:
        ticker_name = "Test_Ticker"
    export_log("Started...", ticker_name, log_file, True)
    
    processor = LS_Detector()
    cur_signal = None
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0:
        fps = 15
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
                        pass
                    else:
                        cur_signal = response_data["signal"]
                        if cur_signal == "L":
                            full_signal = "LONG"
                            L_num += 1
                        else:
                            full_signal = "SHORT"
                            S_num += 1
                        export_log("{}\tLs = {}\tSs = {}".format(full_signal, L_num, S_num), ticker_name, log_file, True)
                if is_show:
                    cv2.imshow('frame', response_data["frame"])
            else:
                export_log("Failed to Process: {}".format(response_data['descript']), ticker_name, log_file, True)
                break
        else:
            export_log("Done process...", ticker_name, log_file, True)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def main(args):
    default_types = ["capture", "camera", "video"]
    input_type = args.input_type
    video_file = args.video
    ticker_config_file = args.config
    is_show = args.show

    assert input_type in default_types

    if input_type == "capture":
        if ticker_config_file is not None and os.path.exists(ticker_config_file):
            with open(ticker_config_file, "r") as t:
                pre_defined_tickers = [tick.strip() for tick in t.readlines() if tick.strip() != ""]
            if len(pre_defined_tickers) == 0:
                print("Empty config file. Please confirm that.")
                return
            print("The existing ticker names are follow:")
            for i, tick in enumerate(pre_defined_tickers):
                print("\t{}:\t{}".format(i, tick))
            
            ticker_name = None
            while True:
                ticker_idx = input("Please select ticker index as integer: ")
                try:
                    ticker_idx = int(ticker_idx)
                    if ticker_idx in range(len(pre_defined_tickers)):
                        ticker_name = pre_defined_tickers[ticker_idx]
                        # print()
                        break
                    else:
                        print("Error: invalid ticker index. Please select again.")
                except ValueError:
                    print("This is invalid index type. Input integer number.")
            if ticker_name is None:
                return
            
        else:
            print("No exists ticker config file. Please check that.")
            return

        print("Capture screen.. \nPlease confirm box boundries and labels")
        rect_prossor = GETRect()
        coordinates = rect_prossor.start()
        if coordinates is None:
            return
        else:
            ticker_info = "Ticker Name: {}\tTicker Coordinates: {}".format(ticker_name, coordinates["bound"])
            
            cap = ScreenCap(coordinates["bound"])
            # ticker_name = coordinates["label"]
            log_file = args.log_file
            if log_file is None:
                log_file = ticker_name + "_" + datetime.now().strftime("%m_%d_%Y") + ".log"

            log_path = os.path.join(log_folder, log_file)
            export_log(ticker_info, ticker_name, log_path)
            ls_detect(cap, is_show, log_path, ticker_name)

    elif input_type == "video":
        cap = cv2.VideoCapture(video_file)
        log_file = args.log_file
        if log_file is None:
            log_file = datetime.now().strftime("%m_%d_%Y") + ".log"

        log_path = os.path.join(log_folder, log_file)

        ls_detect(cap, is_show, log_path)
    elif input_type == "camera":
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
        
        log_file = args.log_file
        if log_file is None:
            log_file = datetime.now().strftime("%m_%d_%Y") + ".log"

        log_path = os.path.join(log_folder, log_file)

        ls_detect(cap, is_show, log_path)

    


if __name__ == "__main__":

    # default="chart line light Right to Left.mov"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input_type", default="capture", help="input type to be processed.")
    parser.add_argument("-c", "--config", default="ticker.config", help="config file path of ticker")

    parser.add_argument("-v", "--video", type=str, help="Path for video file to be processed when input type is video.")
    parser.add_argument("--show", action="store_true", help="Showing process and result frame.")
    parser.add_argument("--log_file", type=str, help="log file path")
    args = parser.parse_args()
    main(args)
