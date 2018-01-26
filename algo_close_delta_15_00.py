import numpy as np
import utils
import config
import datetime


def algo_close_delta_15_00():
    DELTA_H, DELTA_M = config.get_config().ALGO_CLOSE_DELTA_15_00_DELTA_TIME
    DELTA_TIME = config.get_config().RUN_TIME.replace(hour=DELTA_H, minute=DELTA_M, second=0, microsecond=0)

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:

        # get undelying px
        last_bar = utils.get_last_bar(fut_code)

        BAR_4H_S_H, BAR_4H_S_M = config.get_config().ALGO_CLOSE_DELTA_15_00_4H_BAR
        bar = utils.get_specific_bar(fut_code, hour=BAR_4H_S_H, minute=BAR_4H_S_M)

        delta_px = bar.Close
        delta = utils.get_portfolio_delta(fut_code, delta_px, utils.default_time_shift_strategy, DELTA_TIME)

        if bar.Open < bar.Close:
            buy_dist = bar.High - bar.Close
            sell_dist = bar.Close - bar.Open
        elif bar.Close < bar.Open:
            buy_dist = bar.Open - bar.Close
            sell_dist = bar.Close - bar.Low
        else:
            buy_dist = bar.High - bar.Close
            sell_dist = bar.Close - bar.Low


        if (round(delta) > 0 and sell_dist > buy_dist) or (round(delta) < 0 and buy_dist > sell_dist):
            utils.add_stop_orders(fut_code, np.array([bar.Close]), np.array([delta]), order_type='MKT')
            utils.set_order_sequence(np.array([0]))