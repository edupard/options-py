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
        bar_4h = utils.get_specific_bar(fut_code, hour=config.get_config().ALGO_NEWS_4H_START_HOUR)
        bars_5_min = utils.get_bars_range(fut_code,
                                          start_hour=config.get_config().ALGO_NEWS_5M_START_HOUR,
                                          start_minute=config.get_config().ALGO_NEWS_5M_START_MINUTE,
                                          end_hour=config.get_config().ALGO_NEWS_5M_END_HOUR,
                                          end_minute=config.get_config().ALGO_NEWS_5M_END_MINUTE,
                                          duration='5 mins',
                                          )
        bars_1_min = utils.get_bars_range(fut_code,
                                          start_hour=config.get_config().ALGO_NEWS_1M_START_HOUR,
                                          start_minute=config.get_config().ALGO_NEWS_1M_START_MINUTE,
                                          end_hour=config.get_config().ALGO_NEWS_1M_END_HOUR,
                                          end_minute=config.get_config().ALGO_NEWS_1M_END_MINUTE,
                                          duration='1 min',
                                          )
        second_bar_open = bars_5_min.iloc[0].Open
        second_bar_close= bars_1_min.iloc[-1].Close
        second_bar_high = second_bar_open
        second_bar_low = second_bar_open
        for _, bar in bars_5_min.iterrows():
            second_bar_high = max(second_bar_high, bar.High)
        for _, bar in bars_1_min.iterrows():
            second_bar_high = max(second_bar_high, bar.High)

        for _, bar in bars_5_min.iterrows():
            second_bar_low = max(second_bar_low, bar.Low)
        for _, bar in bars_1_min.iterrows():
            second_bar_low = max(second_bar_low, bar.Low)


        if bar_4h.Close > bar_4h.Open:
            high = max(bar_4h.High, second_bar_high)
            low = min(bar_4h.Open, second_bar_low)
        elif bar_4h.Close < bar_4h.Open:
            high = max(bar_4h.Open, second_bar_high)
            low = min(bar_4h.Low, second_bar_low)
        else:
            high = max(bar_4h.High, second_bar_high)
            low = min(bar_4h.Low, second_bar_low)

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
