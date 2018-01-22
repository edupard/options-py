class Config(object):
    def __init__(self):
        # input by utils.py
        self.RUN_TIME = None
        self.positions_df = None
        self.time_bars_df = None
        self.TARGET_ORDERS_FILE = None
        self.SCRIPT_PARAMS = None

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

        # 23_00
        self.STOPS_NUM_23_00 = 3
        self.STOP_PX_STEP_23_00 = 60 / self.FUT_PRICE_COEFF


_config = Config()


def get_config():
    return _config
