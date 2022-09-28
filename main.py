import os
import argparse
from datetime import datetime
import time
from urllib import request

import cv2
from process import LS_Detector
from rect_input import rectangle_select
from capture import ScreenCap
# from trade import process_trade
# from log_utils import export_log
# import configparser
# import json
import requests


def get_config_file_list():
    data = {
        "command": "TICKERS",
        "data": None
    }
    tick_list = []
    try:
        rep_data = requests.get("http://127.0.0.1:8088/config", json=data)
        print(rep_data)
        if rep_data.status_code == 200:
            json_data = rep_data.json()
            if json_data["status"] == "success":
                tick_list = json_data["message"][0]
            else:
                print("Failed to get config file list...\nTry again.")
        else:
            print(request.text)
        return tick_list
    except ConnectionRefusedError as err:
        print("Failed to access: {}".format(repr(err)))
        return []


def send_log(msg, trade_config_path, is_notified=False):
    print(msg)
    try:
        log_data = {
            "message": msg,
            "is_notified": is_notified,
            "config_file": trade_config_path
        }
        data = {
            "command": "EXPORT_LOG",
            "message": log_data
        }
        result = requests.post("http://127.0.0.1:8088/auto_order", json=data)
        print(result.json()["message"][0])
    except:
        print("Failed to export log.")
    
def send_order(order_data: dict):

    try:
        data = {
            "command": "PLACE_ORDER",
            "message": order_data
        }
        result =  requests.post("http://127.0.0.1:8088/auto_order", json=data)
        return result.json()["message"][0]

    except:
        return "Failed to send order request."


def ls_detect(cap, trade_config_path, is_show, is_trade=False):
    # print("hello world!!!!")

    now = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")[:-3]
    msg = "{}\t{}\tScreen Capture Started...".format(now, trade_config_path)

    send_log(msg, trade_config_path, is_notified=True)
    
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
                        msg = "{}\t{}".format(full_signal, L_num + S_num)
                        now = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")[:-3]
                        tm_msg = '{}\t{}\t{}'.format(trade_config_path, now, msg)
                        send_log(tm_msg, trade_config_path, is_notified=True)
                        if is_trade:
                            order_data = {
                                "signal": cur_signal,
                                "ticker": trade_config_path
                            }
                            order_result = send_order(order_data)
                            print("Order Result:\n{}".format(order_result))
                            # if get_global_flag():
                            #     args_order = {
                            #         "contract": {},
                            #         "order": {
                            #             "signal": cur_signal,
                            #             "action": action
                            #         }
                            #     }
                            #     # print(f"{trade_config_path=}")
                            #     result_order = process_trade(args_order, cfg_file=trade_config_path)
                            #     # now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                            #     # tm_msg = '{}\t{}\t{}'.format(ticker_name, now, result_order["description"])
                            #     tm_msg = result_order["description"]
                            #     slack_msg = result_order["slack_msg"]
                            #     export_log(tm_msg, log_file, slack_msg, True)
                            # else:
                            #     print("\tGlobal Trade Disabled...")

                if is_show:
                    cv2.imshow('frame', response_data["frame"])
            else:
                msg = "Failed to Process: {}".format(response_data['descript'])
                now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                tm_msg = '{}\t{}\t{}'.format(trade_config_path, now, msg)
                send_log(tm_msg, trade_config_path, is_notified=True)

                break
        else:
            msg = "Done process..."
            now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            tm_msg = '{}\t{}\t{}'.format(trade_config_path, now, msg)
            send_log(tm_msg, trade_config_path, is_notified=True)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def main(args):
    default_types = ["capture"]
    input_type = args.input_type
    # video_file = args.video
    # ticker_config_file = args.config
    is_show = args.show
    is_trade = args.trade

    assert input_type in default_types
    pre_defined_cfg_files = get_config_file_list()

    if pre_defined_cfg_files == []:
        print("Config file list is empty. Please check it.")
        return

    if input_type == "capture":
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

        print("Capture screen.. \nPlease confirm box boundaries and labels")

        time.sleep(1)
        coordinates = rectangle_select()
        if coordinates is None:
            return
        else:
            ticker_name = ticker_config_file.split(".")[0]
            ticker_info = "Ticker Name: {}\tTicker Coordinates: {}".format(ticker_name, coordinates)
            
            cap = ScreenCap(coordinates)
            # log_file = ticker_name + "_" + datetime.now().strftime("%m_%d_%Y") + ".log"

            # log_path = os.path.join(log_folder, log_file)
            # export_log(ticker_info, log_path)
            # trade_config_path = os.path.join(trade_config_dir, ticker_config_file)
            ls_detect(cap, ticker_config_file, is_show, is_trade)

    
if __name__ == "__main__":

    default="chart line light Right to Left.mov"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input_type", default="capture", help="input type to be processed.")
    # parser.add_argument("-c", "--config", default="ticker.config", help="config file path of ticker")

    # parser.add_argument("-v", "--video", type=str, help="Path for video file to be processed when input type is video.")
    parser.add_argument("--show", action="store_true", help="Showing process and result frame.")
    parser.add_argument("--trade", action="store_true", help="Decide if auto trade is enable or not.")
    args = parser.parse_args()
    main(args)
    # get_work_path()    
