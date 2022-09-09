import os
from datetime import datetime

from order_utils.create_order import get_cfg, place_order


def parse_parameter(direction, action, qty=None, config_qty=0):

    default_direct = ["LS", "LC", "SC"]
    if direction not in default_direct:
        print("Direction must be in {}.\nPlease check config file.".format(default_direct))
        return False, None
    if direction == "LS":
        if action == "BUY":
            if qty is None or qty == 0:
                return True, config_qty
            elif qty > 0:
                return False, None
            else:
                return True, abs(qty) * 2
        elif action == "SELL":
            if qty is None or qty == 0:
                return True, config_qty
            elif qty > 0:
                return False, qty * 2
            else:
                return False, None
    elif direction == "LC":
        if action == "BUY":
            if qty is None or qty == 0:
                return True, config_qty
            else:
                return False, None
        elif action == "SELL":
            if qty is None or qty == 0:
                return False, None
            elif qty > 0:
                return False, qty
            else:
                return False, None
    else:
        if action == "BUY":
            if qty is None or qty == 0:
                return False, None
            elif qty > 0:
                return True, abs(qty)
            else:
                return False, None
        elif action == "SELL":
            if qty is None or qty == 0:
                return True, config_qty
            elif qty > 0:
                return False, None
            else:
                return False, None

    pass


def process_trade(cfg_dict: dict = None, cfg_file=None, is_auto=True):
    res_value = {
        "success": False,
        "description": "",
        "slack_msg": ""
    }
    if cfg_dict is None:
        res_value["description"] = "Invalid config parameter. Please check config."
        return res_value
    else:
        if "contract" in cfg_dict and "order" in cfg_dict:
            pass
        else:
            res_value["description"] = "Invalid config parameter. Please check config."
            return res_value

    if is_auto:
        if cfg_file is None or not os.path.exists(cfg_file):
            res_value["description"] = "Invalid config file. Please check config file."
            return res_value
        try:
            action = cfg_dict["order"]["action"]
            signal = cfg_dict["order"]["signal"]
        except KeyError as err:
            res_value["description"] = "Please check config."
            return res_value
        predefined_order_dict = get_cfg(cfg_file)
        # print(f"{predefined_order_dict=}")
        contract_dict = predefined_order_dict["contract"]

        order_dict = predefined_order_dict["order"]
        order_dict["action"] = action

        config_qty = int(order_dict["qty"])
        direction = order_dict["direction"]

        is_needed, real_qty = parse_parameter(direction, action, config_qty=config_qty)
        if is_needed:
            order_dict["qty"] = real_qty
            open_order, order_status, exec_detail, errors = place_order(contract_dict, order_dict)
            total_log = open_order + order_status + exec_detail + errors
            total_log.sort(key=lambda row: (row[0]))
            log_msg = "\n".join([x[0] + "\t" + x[1] for x in total_log])
            if len(order_status) != 0:
                slack_msg = "Order pre submitted to IB\n{}\t{}".format(order_status[-1][0], order_status[-1][1])
            else:
                slack_msg = "{}\t{}".format(errors[-1][0], errors[-1][1])
            res_value["success"] = True
            res_value["description"] = log_msg
            res_value["slack_msg"] = slack_msg
            return res_value

        else:
            ignore_msg = "Trade Ignored due to already existing position"
            now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            log_msg = "{}\tSymbol: {}\tSec Type{}\tAction: {}\tQTY: {}" \
                      "\t{}".format(now, contract_dict["symbol"], contract_dict["sectype"],
                                    order_dict["action"], order_dict["qty"], ignore_msg)
            # print(ignore_msg)
            res_value["description"] = log_msg
            return res_value
    else:

        if cfg_file is not None and os.path.exists(cfg_file):
            predefined_order_dict = get_cfg(cfg_file)
            contract_dict = predefined_order_dict["contract"]
            order_dict = predefined_order_dict["order"]
        else:
            contract_dict = {},
            order_dict = {}
        for key, value in cfg_dict["order"].items():
            order_dict[key] = value
        for key, value in cfg_dict["contract"].items():
            contract_dict[key] = value

