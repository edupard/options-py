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

        # NIGHT ----------------------------------------------------------------------------------------

        self.ALGO_NIGHT_DELTA_TIME = (1, 0)

        self.ALGO_NIGHT_4H_BAR = (23, 0)


        self.ALGO_NIGHT_UPTREND_BUY_STP = [
            (0, 0, 0, 0, False),
            (0, 1, 30, 0, True),
            (0, 2, 65, 0, True)
        ]

        self.ALGO_NIGHT_UPTREND_SELL_STP = [
            (0, 0, 0, 0, False),
            (0, 0, 0, 0, False),
            (0, 1, 65, 0, True)
        ]

        self.ALGO_NIGHT_DOWNTREND_BUY_STP = [
            (0, 0, 0, 0, False),
            (0, 0, 0, 0, False),
            (0, 3, 65, 0, True)
        ]

        self.ALGO_NIGHT_DOWNTREND_SELL_STP = [
            (0, 0, 0, 0, False),
            (0, 1, 30, 0, True),
            (0, 1, 65, 0, True)
        ]

        # 07_00 -------------------------------------------------------------------------

        self.ALGO_07_00_DELTA_TIME = (7, 0)

        # 02:00 - 03:00
        self.ALGO_07_00_4H_FIRST_BAR = (2, 0)
        # 03:00 - 07:00
        self.ALGO_07_00_4H_SECOND_BAR = (3, 0)

        # [SHIFT_PX, NUM, GRID_STEP_PX, FWD_PX]
        self.ALGO_07_00_BUY_STP = [
            (0, 0, 0, 0, False),
            (10, 3, 15, 15, False),
            (0, 3, 65, 0, True)
        ]

        self.ALGO_07_00_SELL_STP = [
            (0, 0, 0, 0, False),
            (10, 3, 15, 15, False),
            (0, 1, 65, 0, True)
        ]

        # NEWS ------------------------------------------------------------------------------------------------------------------------------

        self.ALGO_NEWS_DELTA_TIME = (15, 0)

        # 11:00 - 15:00
        self.ALGO_NEWS_4H_BAR = (11, 0)
        # 15:00 - 16:25
        self.ALGO_NEWS_5M_RANGE = (15, 0, 16, 20)
        # 16:25 - 16:29
        self.ALGO_NEWS_1M_RANGE = (16, 25, 16, 28)

        # [SHIFT_PX, NUM, GRID_STEP_PX, FWD_PX, IS_SAFE]
        self.ALGO_NEWS_BUY_STP = [
            (5, 1, 45, 45, False),
            (0, 2, 15, 15, False),
            (0, 3, 65, 0, True)
        ]

        self.ALGO_NEWS_SELL_STP = [
            (5, 1, 45, 45, False),
            (0, 2, 15, 15, False),
            (0, 1, 65, 0, True)
        ]
        
        # STAT --------------------------------------------------------------------------------------------------------

        self.ALGO_STAT_DELTA_TIME = (15, 0)

        # 5 m 15:00 - 17:00
        self.ALGO_STAT_5M_RANGE = (15 , 0,  16, 55)

        # [SHIFT_PX, NUM, GRID_STEP_PX, FWD_PX]
        self.ALGO_STAT_BUY_STP = [
            (0, 0, 0, 0, False),
            (0, 3, 15, 15, False),
            (0, 3, 65, 0, True)
        ]

        self.ALGO_STAT_SELL_STP = [
            (0, 0, 0, 0, False),
            (5, 3, 15, 15, False),
            (0, 1, 65, 0, True)
        ]

        # 19:00 --------------------------------------------------------------------------------------------------------
        self.ALGO_19_00_DELTA_TIME = (19, 0)

        # 15:00 - 19:00
        self.ALGO_19_00_4H_BAR = (15, 0)

        # [SHIFT_PX, NUM, GRID_STEP_PX, FWD_PX]
        self.ALGO_19_00_BUY_STP = [
            (0, 0, 0, 0, False),
            (10, 3, 15, 15, False),
            (0, 3, 65, 0, True)
        ]

        self.ALGO_19_00_SELL_STP = [
            (0, 0, 0, 0, False),
            (10, 3, 15, 15, False),
            (0, 1, 65, 0, True)
        ]

        # 11:00 --------------------------------------------------------------------------------------------------------
        self.ALGO_11_00_DELTA_TIME = (11, 0)

        # 02:00 - 03:00
        self.ALGO_11_00_4H_FIRST_BAR = (2, 0)

        # 03:00 - 07:00
        self.ALGO_11_00_4H_SECOND_BAR = (3, 0)

        # 07:00 - 11:00
        self.ALGO_11_00_4H_THIRD_BAR = (7, 0)


        self.ALGO_11_00_DAY_SL = 35

        # [SHIFT_PX, NUM, GRID_STEP_PX, FWD_PX]
        self.ALGO_11_00_BUY_STP = [
            (0, 0, 0, 0, False),
            (10, 3, 15, 15, False),
            (0, 3, 65, 0, True)
        ]

        self.ALGO_11_00_SELL_STP = [
            (0, 0, 0, 0, False),
            (10, 3, 15, 15, False),
            (0, 1, 65, 0, True)
        ]
        
        
        

_config = Config()


def get_config():
    return _config
