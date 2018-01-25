import utils
import config

from main_levels_algo import main_levels_algo

def algo_19_00():
    # shift time
    DELTA_H, DELTA_M = config.get_config().ALGO_19_00_DELTA_TIME
    DELTA_TIME = config.get_config().RUN_TIME.replace(hour=DELTA_H, minute=DELTA_M, second=0, microsecond=0)

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        BAR_4H_S_H, BAR_4H_S_M = config.get_config().ALGO_19_00_4H_BAR

        last_bar = utils.get_last_bar(fut_code)
        last_px = last_bar.Close

        bar = utils.get_specific_bar(fut_code, hour=BAR_4H_S_H, minute=BAR_4H_S_M)

        if bar.Close > bar.Open:
            high = bar.High
            low = bar.Open
        elif bar.Close < bar.Open:
            high = bar.High
            low = bar.Low
        else:
            high = bar.High
            low = bar.Low

        buy_stps = config.get_config().ALGO_19_00_BUY_STP
        sell_stps = config.get_config().ALGO_19_00_SELL_STP

        main_levels_algo(fut_code, high, low, DELTA_TIME, last_px, buy_stps, sell_stps)




