import utils
import config

from fwd_levels_algo import fwd_levels_algo, FwdLevelsAlgoParams

def algo_news():
    # shift time
    DELTA_TIME = config.get_config().RUN_TIME.replace(hour=15, minute=0, second=0, microsecond=0)

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        first_bar = utils.get_specific_bar(fut_code, hour=config.get_config().ALGO_NEWS_FIRST_BAR_START_HOUR)
        second_bar = utils.get_specific_bar(fut_code, hour=config.get_config().ALGO_NEWS_SECOND_BAR_START_HOUR)

        if first_bar.Close > first_bar.Open:
            high = max(first_bar.High, second_bar.High)
            low = min(first_bar.Open, second_bar.Low)
        elif first_bar.Close < first_bar.Open:
            high = max(first_bar.Open, second_bar.High)
            low = min(first_bar.Low, second_bar.Low)
        else:
            high = max(first_bar.High, second_bar.High)
            low = min(first_bar.Low, second_bar.Low)

        last_bar = utils.get_last_bar(fut_code)
        last_px = last_bar.Close

        params = FwdLevelsAlgoParams()

        params.BUY_ROOM = config.get_config().ALGO_NEWS_BUY_ROOM
        params.BUY_FWD = config.get_config().ALGO_NEWS_BUY_FWD
        params.BUY_MAIN_STEP = config.get_config().ALGO_NEWS_BUY_MAIN_STEP
        params.MAIN_BUY_ADD_STOPS = config.get_config().ALGO_NEWS_MAIN_BUY_ADD_STOPS
        params.BUY_ADD_FWD = config.get_config().ALGO_NEWS_BUY_ADD_FWD
        params.BUY_ADD_MAIN_STEP = config.get_config().ALGO_NEWS_BUY_ADD_MAIN_STEP
        params.SAFE_BUY_STOPS = config.get_config().ALGO_NEWS_SAFE_BUY_STOPS
        params.BUY_SAFE_STEP = config.get_config().ALGO_NEWS_BUY_SAFE_STEP
        params.SELL_ROOM = config.get_config().ALGO_NEWS_SELL_ROOM
        params.SELL_FWD = config.get_config().ALGO_NEWS_SELL_FWD
        params.SELL_MAIN_STEP = config.get_config().ALGO_NEWS_SELL_MAIN_STEP
        params.MAIN_SELL_ADD_STOPS = config.get_config().ALGO_NEWS_MAIN_SELL_ADD_STOPS
        params.SELL_ADD_FWD = config.get_config().ALGO_NEWS_SELL_ADD_FWD
        params.SELL_ADD_MAIN_STEP = config.get_config().ALGO_NEWS_SELL_ADD_MAIN_STEP
        params.SAFE_SELL_STOPS = config.get_config().ALGO_NEWS_SAFE_SELL_STOPS
        params.SELL_SAFE_STEP = config.get_config().ALGO_NEWS_SELL_SAFE_STEP

        fwd_levels_algo(fut_code, high, low, DELTA_TIME, last_px, params)
