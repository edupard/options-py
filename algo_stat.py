import utils
import config

from fwd_levels_algo import fwd_levels_algo, FwdLevelsAlgoParams

def algo_stat():
    # shift time
    DELTA_TIME = config.get_config().RUN_TIME.replace(hour=15, minute=0, second=0, microsecond=0)

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        bars_5_min = utils.get_bars_range(fut_code,
                                          start_hour=config.get_config().ALGO_STAT_5M_START_HOUR,
                                          start_minute=config.get_config().ALGO_STAT_5M_START_MINUTE,
                                          end_hour=config.get_config().ALGO_STAT_5M_END_HOUR,
                                          end_minute=config.get_config().ALGO_STAT_5M_END_MINUTE,
                                          duration='5 mins',
                                          )
        bar_open = bars_5_min.iloc[0].Open
        bar_close= bars_5_min.iloc[-1].Close
        bar_high = bar_open
        bar_low = bar_open
        for _, bar in bars_5_min.iterrows():
            bar_high = max(bar_high, bar.High)
        for _, bar in bars_5_min.iterrows():
            bar_low = max(bar_low, bar.Low)

        if bar_close > bar_open:
            high = bar_high
            low = bar_close
        elif bar_close < bar_open:
            high = bar_close
            low = bar_low
        else:
            high = bar_high
            low = bar_low

        last_bar = utils.get_last_bar(fut_code)
        last_px = last_bar.Close

        params = FwdLevelsAlgoParams()

        params.BUY_ROOM = config.get_config().ALGO_STAT_BUY_ROOM
        params.BUY_FWD = config.get_config().ALGO_STAT_BUY_FWD
        params.BUY_MAIN_STEP = config.get_config().ALGO_STAT_BUY_MAIN_STEP
        params.MAIN_BUY_ADD_STOPS = config.get_config().ALGO_STAT_MAIN_BUY_ADD_STOPS
        params.BUY_ADD_FWD = config.get_config().ALGO_STAT_BUY_ADD_FWD
        params.BUY_ADD_MAIN_STEP = config.get_config().ALGO_STAT_BUY_ADD_MAIN_STEP
        params.SAFE_BUY_STOPS = config.get_config().ALGO_STAT_SAFE_BUY_STOPS
        params.BUY_SAFE_STEP = config.get_config().ALGO_STAT_BUY_SAFE_STEP
        params.SELL_ROOM = config.get_config().ALGO_STAT_SELL_ROOM
        params.SELL_FWD = config.get_config().ALGO_STAT_SELL_FWD
        params.SELL_MAIN_STEP = config.get_config().ALGO_STAT_SELL_MAIN_STEP
        params.MAIN_SELL_ADD_STOPS = config.get_config().ALGO_STAT_MAIN_SELL_ADD_STOPS
        params.SELL_ADD_FWD = config.get_config().ALGO_STAT_SELL_ADD_FWD
        params.SELL_ADD_MAIN_STEP = config.get_config().ALGO_STAT_SELL_ADD_MAIN_STEP
        params.SAFE_SELL_STOPS = config.get_config().ALGO_STAT_SAFE_SELL_STOPS
        params.SELL_SAFE_STEP = config.get_config().ALGO_STAT_SELL_SAFE_STEP

        fwd_levels_algo(fut_code, high, low, DELTA_TIME, last_px, params)
