import utils
import config

from main_levels_algo import main_levels_algo

def algo_07_00():
    # shift time
    DELTA_H, DELTA_M = config.get_config().ALGO_07_00_DELTA_TIME
    DELTA_TIME = config.get_config().RUN_TIME.replace(hour=DELTA_H, minute=DELTA_M, second=0, microsecond=0)

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        FIRST_BAR_4H_S_H, FIRST_BAR_4H_S_M = config.get_config().ALGO_07_00_4H_FIRST_BAR
        SECOND_BAR_4H_S_H, SECOND_BAR_4H_S_M = config.get_config().ALGO_07_00_4H_SECOND_BAR


        first_bar = utils.get_specific_bar(fut_code, hour=FIRST_BAR_4H_S_H, minute=FIRST_BAR_4H_S_M)
        second_bar = utils.get_specific_bar(fut_code, hour=SECOND_BAR_4H_S_H, minute=SECOND_BAR_4H_S_M)

        high = max(first_bar.High, second_bar.High)
        low = min(first_bar.Low, second_bar.Low)

        last_bar = utils.get_last_bar(fut_code)
        last_px = last_bar.Close

        buy_stps = config.get_config().ALGO_07_00_BUY_STP
        sell_stps = config.get_config().ALGO_07_00_SELL_STP

        main_levels_algo(fut_code, high, low, DELTA_TIME, last_px, buy_stps, sell_stps)




