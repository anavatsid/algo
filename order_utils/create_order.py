# CREDITS https://tradersacademy.online/trading-topics/trader-workstation-tws/placing-orders
# WORKING CODE VV APR 2022
import os.path
import sys

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from threading import Timer
import configparser


def get_cfg(config_path):
    config = configparser.ConfigParser()
    config.read([config_path])
    _dict_ = {
        "contract": dict(config.items("contract")),
        "order": dict(config.items("order"))
    }
    return _dict_


class OrderAPP(EWrapper, EClient):
    def __init__(self, contract_config: dict, order_config: dict = None):
        EClient.__init__(self, self)
        self.contract_config = contract_config  # get_cfg(contract_config_path)
        self.order_config = order_config
        self.status_result = None

    def error(self, reqId , errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId ):
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId , status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ", Remaining: ", remaining, ", LastFillPrice: ", lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)

    def start(self):
        contract = Contract()
        print(self.contract_config)
        contract.symbol = self.contract_config["symbol"]
        contract.secType = self.contract_config["sectype"]
        contract.exchange = self.contract_config["exchange"]
        contract.currency = self.contract_config["currency"]
        contract.primaryExchange = self.contract_config["primaryexchange"]
        contract.lastTradeDateOrContractMonth = self.contract_config["lasttradedateorcontractmonth"]

        order = Order()
        order.action = "BUY"
        order.totalQuantity = 1
        order.orderType = "MKT"
        order.lmtPrice = 50.0
        order.transmit = True

        self.placeOrder(self.nextOrderId, contract, order)
        # print(self.contract_config["contract"]["asd"])

    def stop(self):
        self.done = True
        self.disconnect()



def place_order(contract_dict: dict, order_dict: dict):

    app = OrderAPP(contract_dict, order_dict)
    app.nextOrderId = 0
    app.connect("127.0.0.1", 4002, 11)

    Timer(3, app.stop).start()

    app.run()
    pass


if __name__ == "__main__":

    order_config = {}
    config_file = sys.argv[1]
    if not os.path.exists(config_file):
        print("No exists such file: {}".format(config_file))
    else:
        contract_config = get_cfg(config_file)
        sys.exit(place_order(contract_config, order_config))
