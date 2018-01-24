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
        self.NIGTH_BAR_START_HOUR = 23

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

        # 07_00
        self.ALGO_07_00_FIRST_BAR_START_HOUR = 2
        self.ALGO_07_00_SECOND_BAR_START_HOUR = 3

        # buy
        # first
        self.ALGO_07_00_BUY_ROOM = 10 / self.FUT_PRICE_COEFF
        self.ALGO_07_00_BUY_FWD = 50 / self.FUT_PRICE_COEFF
        self.ALGO_07_00_BUY_MAIN_STEP = 50 / self.FUT_PRICE_COEFF # or 15 (step to find first non-zero delta)
        # additional
        self.ALGO_07_00_MAIN_BUY_ADD_STOPS = 2
        self.ALGO_07_00_BUY_ADD_FWD = 15 / self.FUT_PRICE_COEFF
        self.ALGO_07_00_BUY_ADD_MAIN_STEP = 15 / self.FUT_PRICE_COEFF # grid step !!!
        # safe
        self.ALGO_07_00_SAFE_BUY_STOPS = 3
        self.ALGO_07_00_BUY_SAFE_STEP = 65 / self.FUT_PRICE_COEFF

        # sell
        # first
        self.ALGO_07_00_SELL_ROOM = 10 / self.FUT_PRICE_COEFF
        self.ALGO_07_00_SELL_FWD = 50 / self.FUT_PRICE_COEFF
        self.ALGO_07_00_SELL_MAIN_STEP = 50 / self.FUT_PRICE_COEFF # or 15 (step to find first non-zero delta)
        # additional
        self.ALGO_07_00_MAIN_SELL_ADD_STOPS = 2
        self.ALGO_07_00_SELL_ADD_FWD = 15 / self.FUT_PRICE_COEFF
        self.ALGO_07_00_SELL_ADD_MAIN_STEP = 15 / self.FUT_PRICE_COEFF # grid step !!!
        # safe
        self.ALGO_07_00_SAFE_SELL_STOPS = 1
        self.ALGO_07_00_SELL_SAFE_STEP = 65 / self.FUT_PRICE_COEFF

        # NEWS
        self.ALGO_NEWS_FIRST_BAR_START_HOUR = 11
        self.ALGO_NEWS_SECOND_BAR_START_HOUR = 15

        # buy
        # first
        self.ALGO_NEWS_BUY_ROOM = 10 / self.FUT_PRICE_COEFF
        self.ALGO_NEWS_BUY_FWD = 50 / self.FUT_PRICE_COEFF
        self.ALGO_NEWS_BUY_MAIN_STEP = 50 / self.FUT_PRICE_COEFF  # or 15 (step to find first non-zero delta)
        # additional
        self.ALGO_NEWS_MAIN_BUY_ADD_STOPS = 2
        self.ALGO_NEWS_BUY_ADD_FWD = 15 / self.FUT_PRICE_COEFF
        self.ALGO_NEWS_BUY_ADD_MAIN_STEP = 15 / self.FUT_PRICE_COEFF  # grid step !!!
        # safe
        self.ALGO_NEWS_SAFE_BUY_STOPS = 3
        self.ALGO_NEWS_BUY_SAFE_STEP = 65 / self.FUT_PRICE_COEFF

        # sell
        # first
        self.ALGO_NEWS_SELL_ROOM = 10 / self.FUT_PRICE_COEFF
        self.ALGO_NEWS_SELL_FWD = 50 / self.FUT_PRICE_COEFF
        self.ALGO_NEWS_SELL_MAIN_STEP = 50 / self.FUT_PRICE_COEFF  # or 15 (step to find first non-zero delta)
        # additional
        self.ALGO_NEWS_MAIN_SELL_ADD_STOPS = 2
        self.ALGO_NEWS_SELL_ADD_FWD = 15 / self.FUT_PRICE_COEFF
        self.ALGO_NEWS_SELL_ADD_MAIN_STEP = 15 / self.FUT_PRICE_COEFF  # grid step !!!
        # safe
        self.ALGO_NEWS_SAFE_SELL_STOPS = 1
        self.ALGO_NEWS_SELL_SAFE_STEP = 65 / self.FUT_PRICE_COEFF
        
        
        

_config = Config()


def get_config():
    return _config
