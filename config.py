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

        # BASIC ---------------------------------------------------------------------------------------------
        self.STOPS_NUM_BASIC = 3
        self.STOP_PX_STEP_BASIC = 60 / self.FUT_PRICE_COEFF

        # ZERO ---------------------------------------------------------------------------------------------
        # (working from zero_delta level or nearest strike)

        #self.ALGO_ZERO_BUY_START = [65]
        #self.ALGO_ZERO_BUY_STP_1 = [3, 65, 0]
        #self.ALGO_ZERO_BUY_STP_2 = [0, 0, 0]
        #self.ALGO_ZERO_BUY_STP_3 = [0, 0, 0]

        # self.ALGO_ZERO_SELL_START = [65]
        # self.ALGO_ZERO_SELL_STP_1 = [3, 65, 0]
        # self.ALGO_ZERO_SELL_STP_2 = [0, 0, 0]
        # self.ALGO_ZERO_SELL_STP_3 = [0, 0, 0]

        # SAFE ---------------------------------------------------------------------------------------------
        # (working from last_bar close level)

        # self.ALGO_SAFE_BUY_START = [65]
        # self.ALGO_SAFE_BUY_STP_1 = [3, 65, 0]
        # self.ALGO_SAFE_BUY_STP_2 = [0, 0, 0]
        # self.ALGO_SAFE_BUY_STP_3 = [0, 0, 0]

        # self.ALGO_SAFE_SELL_START = [65]
        # self.ALGO_SAFE_SELL_STP_1 = [3, 65, 0]
        # self.ALGO_SAFE_SELL_STP_2 = [0, 0, 0]
        # self.ALGO_SAFE_SELL_STP_3 = [0, 0, 0]

        # NIGHT ----------------------------------------------------------------------------------------

        # [NIGHT_BAR_START_HOUR]
        # self.NIGHT_4H = [23]

        # [HEDGING_PARAMS]
        # self.ALGO_NIGHT_BUY_START = [65]
        # self.ALGO_NIGHT_BUY_STP_1 = [1, 15, 15]
        # self.ALGO_NIGHT_BUY_STP_2 = [0, 15, 15]
        # self.ALGO_NIGHT_BUY_STP_3 = [3, 65, 0]

        # self.ALGO_NIGHT_SELL_START = [30]
        # self.ALGO_NIGHT_SELL_STP_1 = [1, 15, 0]
        # self.ALGO_NIGHT_SELL_STP_2 = [0, 15, 15]
        # self.ALGO_NIGHT_SELL_STP_3 = [1, 65, 0]

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

        # 07_00 -------------------------------------------------------------------------

        # 02:00 - 03:00
        self.ALGO_07_00_4H_FIRST_BAR = (2, 0)
        # 03:00 - 07:00
        self.ALGO_07_00_4H_SECOND_BAR = (3, 0)

        # [SHIFT_PX, NUM, GRID_STEP_PX, FWD_PX]
        self.ALGO_07_00_BUY_STP = [
            (0, 0, 0, 0),
            (10, 3, 15, 15),
            (0, 3, 65, 0)
        ]

        self.ALGO_07_00_SELL_STP = [
            (0, 0, 0, 0),
            (10, 3, 15, 15),
            (0, 1, 65, 0)
        ]

        # NEWS ------------------------------------------------------------------------------------------------------------------------------

        # 11:00 - 15:00
        self.ALGO_NEWS_4H_BAR = (11, 0)
        # 15:00 - 16:25
        self.ALGO_NEWS_5M_RANGE = (15, 0, 16, 20)
        # 16:25 - 16:29
        self.ALGO_NEWS_1M_RANGE = (16, 25, 16, 28)

        # [SHIFT_PX, NUM, GRID_STEP_PX, FWD_PX]
        self.ALGO_NEWS_BUY_STP = [
            (5, 1, 45, 45),
            (0, 2, 15, 15),
            (0, 3, 65, 0)
        ]

        self.ALGO_NEWS_SELL_STP = [
            (5, 1, 45, 45),
            (0, 2, 15, 15),
            (0, 1, 65, 0)
        ]
        
        # STAT --------------------------------------------------------------------------------------------------------

        # 5 m 15:00 - 17:00
        self.ALGO_STAT_5M_RANGE = (15 , 0,  16, 55)

        # [SHIFT_PX, NUM, GRID_STEP_PX, FWD_PX]
        self.ALGO_STAT_BUY_STP = [
            (0, 0, 0, 0),
            (0, 3, 15, 15),
            (0, 3, 65, 0)
        ]

        self.ALGO_STAT_SELL_STP = [
            (0, 0, 0, 0),
            (5, 3, 15, 15),
            (0, 1, 65, 0)
        ]
        
        
        

_config = Config()


def get_config():
    return _config
