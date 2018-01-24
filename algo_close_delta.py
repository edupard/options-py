import numpy as np
import utils
import config


def algo_close_delta():
    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        # get undelying px
        last_bar = utils.get_last_bar(fut_code)
        under_px = last_bar.Close

        px_grid = np.zeros((1))
        px_grid[0] = under_px
        delta_grid = utils.get_portfolio_delta_on_grid(fut_code, px_grid, utils.default_time_shift_strategy, config.get_config().RUN_TIME)
        utils.add_stop_orders(fut_code, px_grid, delta_grid, order_type='MKT')
        utils.set_order_sequence(np.array([0]))