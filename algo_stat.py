import utils
import config

from main_levels_algo import main_levels_algo

def algo_stat():
    # shift time
    DELTA_H, DELTA_M = config.get_config().ALGO_STAT_DELTA_TIME
    DELTA_TIME = config.get_config().RUN_TIME.replace(hour=DELTA_H, minute=DELTA_M, second=0, microsecond=0)

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        M5_S_H, M5_S_M, M5_E_H, M5_E_M = config.get_config().ALGO_STAT_5M_RANGE

        bars_5_min = utils.get_bars_range(fut_code,
                                          start_hour=M5_S_H,
                                          start_minute=M5_S_M,
                                          end_hour=M5_E_H,
                                          end_minute=M5_E_M,
                                          duration='5 mins',
                                          )
        bar_open = bars_5_min.iloc[0].Open
        bar_close= bars_5_min.iloc[-1].Close
        bar_high = bar_open
        bar_low = bar_open
        for _, bar in bars_5_min.iterrows():
            bar_high = max(bar_high, bar.High)
        for _, bar in bars_5_min.iterrows():
            bar_low = min(bar_low, bar.Low)

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

        buy_stps = config.get_config().ALGO_STAT_BUY_STP
        sell_stps = config.get_config().ALGO_STAT_SELL_STP

        main_levels_algo(fut_code, high, low, DELTA_TIME, last_px, buy_stps, sell_stps)
