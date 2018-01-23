class Config(object):
    def __init__(self):
        # input by utils.py
        self.RUN_TIME = None
        self.positions_df = None
        self.time_bars_df = None
        self.TARGET_ORDERS_FILE = None
        self.SCRIPT_PARAMS = None
        self.UPTREND = False

        # output
        self.target_order_idx = []
        self.target_code = []
        self.target_qty = []
        self.target_px = []
        self.target_order_type = []

        # constants
        self.FUT_MULT = 1000
        self.OPT_MULT = 1000
        self.YEAR_DAYS_COUNT = 360
        self.FUT_PRICE_COEFF = 320
        self.PRICE_STEP = 5 / self.FUT_PRICE_COEFF
        self.GRID_PX_STEP = 0.07
        self.PROFILE_STEPS = 10
        self.STRIKE_STEP = 0.25

        # basic
        self.STOPS_NUM_BASIC = 3
        self.STOP_PX_STEP_BASIC = 60 / self.FUT_PRICE_COEFF

        # night_stops
        self.STOPS_NUM_NIGHT_BUY = 1
        self.STOPS_NUM_NIGHT_SELL = 1

        self.STOPS_NUM_NIGHT_SAFE_BUY = 3
        self.STOPS_NUM_NIGHT_SAFE_SELL = 1

        self.STOP_PX_STEP_NIGHT_BUY = 30 / self.FUT_PRICE_COEFF
        self.STOP_PX_STEP_NIGHT_SELL = 30 / self.FUT_PRICE_COEFF

        self.STOP_PX_STEP_NIGHT_SAFE_BUY = 60 / self.FUT_PRICE_COEFF
        self.STOP_PX_STEP_NIGHT_SAFE_SELL = 60 / self.FUT_PRICE_COEFF

        self.STOP_PX_STEP_NIGHT_FWD_BUY = 10 / self.FUT_PRICE_COEFF
        self.STOP_PX_STEP_NIGHT_FWD_SELL = 10 / self.FUT_PRICE_COEFF

        # 07:00


_config = Config()


def get_config():
    return _config
