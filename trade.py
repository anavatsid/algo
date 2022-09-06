import os
from order_utils.create_order import get_cfg, place_order


def process_trade(cfg_dict: dict = None, cfg_file=None, is_auto=True):
    if cfg_dict is None:
        print("Invalid config parameter. Please check config")
        return None
    else:
        if "contract" in cfg_dict and "order" in cfg_dict:
            pass
        else:
            print("Invalid config parameter. Please check config")
            return None

    if is_auto:
        if cfg_file is None or not os.path.exists(cfg_file):
            print("Invalid config parameter. Please check config")
            return None
        try:
            action = cfg_dict["order"]["action"]
        except KeyError as err:
            return None
        predefined_order_dict = get_cfg(cfg_file)
        # print(f"{predefined_order_dict=}")
        contract_dict = predefined_order_dict["contract"]

        order_dict = predefined_order_dict["order"]
        order_dict["action"] = action

        place_order(contract_dict, order_dict)
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

