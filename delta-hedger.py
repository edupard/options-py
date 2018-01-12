import pandas as pd
import numpy as np

import utils
import config

utils.parse_input()

target_code = []
target_qty = []
target_px = []
target_order_type = []

def algo_A():
    return None

def algo_B():
    return None

def default_algo():
    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = positions_df[positions_df.SecType == 'FOP'].Underlying.unique()

    for fut_code in fut_codes:
        # sort all fut timebars
        sorted_bars = time_bars_df[time_bars_df.Code == fut_code].sort_values(by='DateTime')
        # get last bar
        last_bar = sorted_bars.iloc[-1]
        # get undelying px
        under_px = last_bar.Close

        def add_stop_orders(px_grid, delta_grid):
            closed_delta = 0
            for i in range(delta_grid.shape[0]):
                order_delta = round(-delta_grid[i] + closed_delta)
                closed_delta -= order_delta
                # create target order
                target_code.append(fut_code)
                target_qty.append(order_delta)
                target_px.append(px_grid[i])
                target_order_type.append('STP')

        px_grid = np.zeros([config.get_config().NUM_BUY_STOPS])
        stop_px = under_px
        for i in range(config.get_config().NUM_BUY_STOPS):
            stop_px += config.get_config().BUY_STOP_PX_STEP
            px_grid[i] = stop_px

        delta_grid, _, _ = utils.get_portfolio_params(fut_code, px_grid)
        add_stop_orders(px_grid, delta_grid)

        px_grid = np.zeros([config.get_config().NUM_BUY_STOPS])
        stop_px = under_px
        for i in range(config.get_config().NUM_SELL_STOPS):
            stop_px -= config.get_config().SELL_STOP_PX_STEP
            px_grid[i] = stop_px

        delta_grid, _, _ = utils.get_portfolio_params(fut_code, px_grid)
        add_stop_orders(px_grid, delta_grid)

if config.get_config().SCRIPT_PARAMS == "default":
    default_algo()
elif config.get_config().SCRIPT_PARAMS == "A":
    algo_A()
elif config.get_config().SCRIPT_PARAMS == "B":
    algo_B()

target_orders_df = pd.DataFrame({
    'code': target_code,
    'qty': target_qty,
    'px': target_px,
    'view_px' : utils.convert_to_view_px_array(target_px),
    'type': target_order_type
})

target_orders_df.to_csv(config.get_config().TARGET_ORDERS_FILE,index=False)
