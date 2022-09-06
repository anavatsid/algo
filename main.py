import os
import argparse
from datetime import datetime
import time

import cv2
from camera_utils import check_camera_idx
from process import LS_Detector
from notifier import send_notification_api
from rect_input import rectangle_select
from capture import ScreenCap
from trade import process_trade

log_folder = "log"
os.makedirs(log_folder, exist_ok=True)

trade_config_dir = "order_utils/cfg"


def get_config_file_list():

    files = [file for file in os.listdir(trade_config_dir) if file.endswith(".cfg")]
    print(files)
    return files


def export_log(msg, ticker_name, log_path, is_notified=False):
    now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    tm_msg = '{}\t{}\t{}'.format(ticker_name, now, msg)
    print(tm_msg)

    with open(log_path, "a") as f:
        f.write('{}\n'.format(tm_msg))
        
        if is_notified:
            ret = send_notification_api(tm_msg)
            f.write('{}\t{}\t{}\n'.format(ticker_name, now, ret))


def ls_detect(cap, is_show, log_file, ticker_name=None, is_trade=False, trade_config_path=None):
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
                            action = "BUY"
                        else:
                            full_signal = "SHORT"
                            S_num += 1
                            action = "SELL"
                        export_log("{}\tLs = {}\tSs = {}".format(full_signal, L_num, S_num), ticker_name, log_file, True)
                        if is_trade:
                            args_order = {
                                "contract": {},
                                "order": {
                                    "action": action
                                }
                            }
                            print(f"{trade_config_path=}")
                            process_trade(args_order, cfg_file=trade_config_path)
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
    # ticker_config_file = args.config
    is_show = args.show
    is_trade = args.trade

    assert input_type in default_types

    if input_type == "capture":
        pre_defined_cfg_files = get_config_file_list()
        if pre_defined_cfg_files is not None and pre_defined_cfg_files != []:
            # with open(ticker_config_file, "r") as t:
            #     pre_defined_tickers = [tick.strip() for tick in t.readlines() if tick.strip() != ""]
            # if len(pre_defined_tickers) == 0:
            #     print("Empty config file. Please confirm that.")
            #     return
            print("The existing ticker names are follow:")
            for i, tick in enumerate(pre_defined_cfg_files):
                print("\t{}:\t{}".format(i, tick))
            
            while True:
                ticker_idx = input("Please select ticker index as integer: ")
                try:
                    ticker_idx = int(ticker_idx)
                    if ticker_idx in range(len(pre_defined_cfg_files)):
                        ticker_config_file = pre_defined_cfg_files[ticker_idx]
                        # print()
                        break
                    else:
                        print("Error: invalid ticker index. Please select again.")
                except ValueError:
                    print("This is invalid index type. Input integer number.")
            if ticker_config_file is None:
                return
            
        else:
            print("No exists config files. Please check that.")
            return

        print("Capture screen.. \nPlease confirm box boundries and labels")
        coordinates = rectangle_select()
        if coordinates is None:
            return
        else:
            ticker_name = ticker_config_file.split(".")[0]
            ticker_info = "Ticker Name: {}\tTicker Coordinates: {}".format(ticker_name, coordinates)
            
            cap = ScreenCap(coordinates)
            log_file = ticker_name + "_" + datetime.now().strftime("%m_%d_%Y") + ".log"

            log_path = os.path.join(log_folder, log_file)
            export_log(ticker_info, ticker_name, log_path)
            trade_config_path = os.path.join(trade_config_dir, ticker_config_file)
            ls_detect(cap, is_show, log_path, ticker_name, is_trade, trade_config_path)

    elif input_type == "video":
        cap = cv2.VideoCapture(video_file)
        log_file = args.log_file
        if log_file is None:
            log_file = datetime.now().strftime("%m_%d_%Y") + ".log"

        log_path = os.path.join(log_folder, log_file)

        ls_detect(cap, is_show, log_path)
    elif input_type == "camera":
        cam_idx = check_camera_idx()
        # if log_file is None:
        log_file = datetime.now().strftime("%m_%d_%Y") + ".log"
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
    # parser.add_argument("-c", "--config", default="ticker.config", help="config file path of ticker")

    parser.add_argument("-v", "--video", type=str, help="Path for video file to be processed when input type is video.")
    parser.add_argument("--show", action="store_true", help="Showing process and result frame.")
    parser.add_argument("--trade", action="store_true", help="process to trade")
    args = parser.parse_args()
    main(args)
