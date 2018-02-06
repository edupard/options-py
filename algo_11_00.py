import utils
import config

from main_levels_algo import main_levels_algo


def algo_11_00():
    # shift time
    DELTA_H, DELTA_M = config.get_config().ALGO_11_00_DELTA_TIME
    DELTA_TIME = config.get_config().RUN_TIME.replace(hour=DELTA_H, minute=DELTA_M, second=0, microsecond=0)

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        FIRST_BAR_4H_S_H, FIRST_BAR_4H_S_M = config.get_config().ALGO_11_00_4H_FIRST_BAR
        SECOND_BAR_4H_S_H, SECOND_BAR_4H_S_M = config.get_config().ALGO_11_00_4H_SECOND_BAR
        THIRD_BAR_4H_S_H, THIRD_BAR_4H_S_M = config.get_config().ALGO_11_00_4H_THIRD_BAR

        last_bar = utils.get_last_bar(fut_code)
        last_px = last_bar.Close

        bar_1 = utils.get_specific_bar(fut_code, hour=FIRST_BAR_4H_S_H, minute=FIRST_BAR_4H_S_M)
        bar_2 = utils.get_specific_bar(fut_code, hour=SECOND_BAR_4H_S_H, minute=SECOND_BAR_4H_S_M)
        bar_3 = utils.get_specific_bar(fut_code, hour=THIRD_BAR_4H_S_H, minute=THIRD_BAR_4H_S_M)

        day_low_2 = min(bar_1.Low, bar_2.Low)
        day_high_2 = max(bar_1.High, bar_2.High)

        day_low_3 = min(bar_1.Low, bar_2.Low, bar_3.Low)
        day_high_3 = max(bar_1.High, bar_2.High, bar_3.High)

        # if bar_3.Close > bar_3.Open and bar_2.Close > bar_2.Open and bar_3.Close > bar_2.Close:
        if bar_3.Low <= day_low_2 and bar_3.Close >= bar_2.Close and bar_3.Low != bar_3.High:
            high = bar_3.High
            low = bar_3.Low
            # low = day_low - config.get_config().ALGO_11_00_DAY_SL / config.get_config().FUT_PRICE_COEFF
        elif bar_3.High >= day_high_2 and bar_3.Close <= bar_2.Close and bar_3.Low != bar_3.High:
            high = bar_3.High
            low = bar_3.Low
        else:
            high = bar_3.High
            low = bar_3.Low

        buy_stps = config.get_config().ALGO_11_00_BUY_STP
        sell_stps = config.get_config().ALGO_11_00_SELL_STP

        main_levels_algo(fut_code, high, low, DELTA_TIME, last_px, buy_stps, sell_stps)
