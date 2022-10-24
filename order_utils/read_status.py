from decimal import Decimal


def read_positions():  # read all accounts positions and return DataFrame with information

    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper
    from ibapi.common import TickerId
    from threading import Thread

    import pandas as pd
    import time

    class ib_class(EWrapper, EClient):

        def __init__(self):
            EClient.__init__(self, self)

            self.all_positions = pd.DataFrame([], columns=['Account', 'Symbol', 'Quantity', 'Average Cost', 'Sec Type'])

        def error(self, reqId: TickerId, errorCode: int, errorString: str):
            if reqId > -1:
                print("Error. Id: ", reqId, " Code: ", errorCode, " Msg: ", errorString)

        def position(self, account, contract, pos, avgCost):
            index = str(account) + str(contract.symbol)
            self.all_positions.loc[index] = account, contract.symbol, pos, avgCost, contract.secType

        def pnl(self, reqId: int, dailyPnL: float,
                      unrealizedPnL: float, realizedPnL: float):
            super().pnl(reqId, dailyPnL, unrealizedPnL, realizedPnL)
            print("Daily PnL Single. ReqId:", reqId, "Position:", "DailyPnL:", dailyPnL, "UnrealizedPnL:",
                  unrealizedPnL, "RealizedPnL:", realizedPnL, "Value:", )

    def run_loop():
        app.run()

    app = ib_class()
    app.connect('127.0.0.1', 4002, 11)
    # Start the socket in a thread
    api_thread = Thread(target=run_loop, daemon=True)
    api_thread.start()
    time.sleep(5)  # Sleep interval to allow time for connection to server

    app.reqPositions()  # associated callback: position
    print("Waiting for IB's API response for accounts positions requests...\n")
    time.sleep(3)
    current_positions = app.all_positions
    current_positions.set_index('Account', inplace=True, drop=True)  # set all_positions DataFrame index to "Account"

    app.disconnect()

    return current_positions


def read_navs():  # read all accounts NAVs

    from ibapi.client import EClient
    from ibapi.wrapper import EWrapper
    from ibapi.common import TickerId
    from threading import Thread

    import pandas as pd
    import time

    class ib_class(EWrapper, EClient):

        def __init__(self):
            EClient.__init__(self, self)

            self.all_accounts = pd.DataFrame([], columns=['reqId', 'Account', 'Tag', 'Value', 'Currency'])

        def error(self, reqId: TickerId, errorCode: int, errorString: str):
            if reqId > -1:
                print("Error. Id: ", reqId, " Code: ", errorCode, " Msg: ", errorString)

        def accountSummary(self, reqId, account, tag, value, currency):
            index = str(account)
            self.all_accounts.loc[index] = reqId, account, tag, value, currency

    def run_loop():
        app.run()

    app = ib_class()
    app.connect('127.0.0.1', 4002, 11)
    # Start the socket in a thread
    api_thread = Thread(target=run_loop, daemon=True)
    api_thread.start()
    time.sleep(1)  # Sleep interval to allow time for connection to server

    app.reqAccountSummary(0, "All",
                          "NetLiquidation")  # associated callback: accountSummary / Can use "All" up to 50 accounts; after that might need to use specific group name(s) created on TWS workstation
    print("Waiting for IB's API response for NAVs requests...\n")
    time.sleep(3)
    current_nav = app.all_accounts

    app.disconnect()

    return (current_nav)


if __name__ == "__main__":
    print("Testing IB's API as an imported library:")

    all_positions = read_positions()
    print(all_positions)
    print()
    all_navs = read_navs()
    print(all_navs)
