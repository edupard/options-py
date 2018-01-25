import numpy as np
import utils
import config

from main_levels_algo import main_levels_algo


def algo_night():
    DELTA_H, DELTA_M = config.get_config().ALGO_NIGHT_DELTA_TIME
    DELTA_TIME = config.get_config().RUN_TIME.replace(hour=DELTA_H, minute=DELTA_M, second=0, microsecond=0)

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        # specific bar

        BAR_4H_S_H, BAR_4H_S_M = config.get_config().ALGO_NIGHT_4H_BAR

        last_bar = utils.get_last_bar(fut_code)
        if last_bar.DateTime.hour != BAR_4H_S_H:
            exit(1)

        last_px = last_bar.Close
        close_px = last_bar.Close


        if config.get_config().UPTREND:
            buy_stps = config.get_config().ALGO_NIGHT_UPTREND_BUY_STP
            sell_stps = config.get_config().ALGO_NIGHT_UPTREND_SELL_STP
        else:
            buy_stps = config.get_config().ALGO_NIGHT_DOWNTREND_BUY_STP
            sell_stps = config.get_config().ALGO_NIGHT_DOWNTREND_SELL_STP

        main_levels_algo(fut_code, close_px, close_px, DELTA_TIME, last_px, buy_stps, sell_stps)
