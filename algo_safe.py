import utils
import config

from main_levels_algo import main_levels_algo


def algo_safe():
    DELTA_TIME = config.get_config().RUN_TIME

    # find all futures
    positions_df = config.get_config().positions_df
    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        last_bar = utils.get_last_bar(fut_code)
        last_px = last_bar.Close

        high = last_px
        low = last_px

        buy_stps = config.get_config().ALGO_SAFE_BUY_STP
        sell_stps = config.get_config().ALGO_SAFE_SELL_STP

        main_levels_algo(fut_code, high, low, DELTA_TIME, last_px, buy_stps, sell_stps)
