class Config(object):
    def __init__(self):
        self.RUN_TIME = None
        self.positions_df = None
        self.time_bars_df = None
        self.TARGET_ORDERS_FILE = None
        self.SCRIPT_PARAMS = None

        self.YEAR_DAYS_COUNT = 360
        self.FUT_PRICE_COEFF = 320
        self.PRICE_STEP = 5 / 320
        self.GRID_PX_STEP = 0.07
        self.PROFILE_STEPS = 10

        #hedger params
        self.NUM_BUY_STOPS = 5
        self.BUY_STOP_PX_STEP = 15 / self.FUT_PRICE_COEFF
        self.NUM_SELL_STOPS = 5
        self.SELL_STOP_PX_STEP = 15 / self.FUT_PRICE_COEFF


_config = Config()

def get_config():
    return _config