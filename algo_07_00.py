import utils
import config

from fwd_levels_algo import fwd_levels_algo, FwdLevelsAlgoParams

def algo_07_00():
    # shift time
    DELTA_TIME = config.get_config().RUN_TIME.replace(hour=7, minute=0, second=0, microsecond=0)

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        first_bar = utils.get_specific_bar(fut_code, hour=config.get_config().ALGO_07_00_FIRST_BAR_START_HOUR)
        second_bar = utils.get_specific_bar(fut_code, hour=config.get_config().ALGO_07_00_SECOND_BAR_START_HOUR)

        high = max(first_bar.High, second_bar.High)
        low = min(first_bar.Low, second_bar.Low)

        last_bar = utils.get_last_bar(fut_code)
        last_px = last_bar.Close

        params = FwdLevelsAlgoParams()

        params.BUY_ROOM = config.get_config().ALGO_07_00_BUY_ROOM
        params.BUY_FWD = config.get_config().ALGO_07_00_BUY_FWD
        params.BUY_MAIN_STEP = config.get_config().ALGO_07_00_BUY_MAIN_STEP
        params.MAIN_BUY_ADD_STOPS = config.get_config().ALGO_07_00_MAIN_BUY_ADD_STOPS
        params.BUY_ADD_FWD = config.get_config().ALGO_07_00_BUY_ADD_FWD
        params.BUY_ADD_MAIN_STEP = config.get_config().ALGO_07_00_BUY_ADD_MAIN_STEP
        params.SAFE_BUY_STOPS = config.get_config().ALGO_07_00_SAFE_BUY_STOPS
        params.BUY_SAFE_STEP = config.get_config().ALGO_07_00_BUY_SAFE_STEP
        params.SELL_ROOM = config.get_config().ALGO_07_00_SELL_ROOM
        params.SELL_FWD = config.get_config().ALGO_07_00_SELL_FWD
        params.SELL_MAIN_STEP = config.get_config().ALGO_07_00_SELL_MAIN_STEP
        params.MAIN_SELL_ADD_STOPS = config.get_config().ALGO_07_00_MAIN_SELL_ADD_STOPS
        params.SELL_ADD_FWD = config.get_config().ALGO_07_00_SELL_ADD_FWD
        params.SELL_ADD_MAIN_STEP = config.get_config().ALGO_07_00_SELL_ADD_MAIN_STEP
        params.SAFE_SELL_STOPS = config.get_config().ALGO_07_00_SAFE_SELL_STOPS
        params.SELL_SAFE_STEP = config.get_config().ALGO_07_00_SELL_SAFE_STEP

        fwd_levels_algo(fut_code, high, low, DELTA_TIME, last_px, params)




