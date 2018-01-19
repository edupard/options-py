import numpy as np
import utils
import config


def basic_algo():
    stops_num = config.get_config().STOPS_NUM

    target_order_idx = []
    target_code = []
    target_qty = []
    target_px = []
    target_order_type = []

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    def add_stop_orders(px_grid, delta_grid, order_type = 'STP'):
        closed_delta = 0
        for i in range(delta_grid.shape[0]):
            order_delta = round(-delta_grid[i] + closed_delta)
            closed_delta -= order_delta
            # create target order
            target_code.append(fut_code)
            target_qty.append(order_delta)
            target_px.append(px_grid[i])
            target_order_type.append(order_type)

    base_order_idx = 0

    def set_order_sequence(order_idxs):
        nonlocal  base_order_idx
        for order_idx in order_idxs:
            target_order_idx.append(base_order_idx + order_idx)
        base_order_idx += order_idxs.shape[0]

    for fut_code in fut_codes:

        # get undelying px
        last_bar = utils.get_last_bar(fut_code)
        under_px = last_bar.Close


        strikes = positions_df[positions_df.Underlying == fut_code].Strike.values
        if strikes.shape[0] == 0:
            #push delta hedging order
            px_grid = np.zeros((1))
            px_grid[0] = under_px
            delta_grid = utils.get_portfolio_delta(fut_code, px_grid, utils.default_time_shift_strategy)
            add_stop_orders(px_grid, delta_grid, order_type='MKT')
            set_order_sequence([0])
            continue

        min_strike = np.min(strikes)
        max_strike = np.max(strikes)

        strike_step = config.get_config().STRIKE_STEP
        min_px_step = config.get_config().PRICE_STEP
        lower_bound = min_strike - strike_step
        upper_bound = max_strike + strike_step
        steps = (upper_bound - lower_bound) / min_px_step + 1

        px_grid = np.linspace(lower_bound, upper_bound, steps)

        delta_grid = utils.get_portfolio_delta(fut_code, px_grid, utils.default_time_shift_strategy)
        roll_right_signs = np.sign(delta_grid) * np.sign(np.roll(delta_grid, 1))
        roll_right_mask = roll_right_signs <= 0
        roll_right_mask = roll_right_mask[1:]

        roll_left_signs = np.sign(delta_grid) * np.sign(np.roll(delta_grid, -1))
        roll_left_mask = roll_left_signs <= 0
        roll_left_mask = roll_left_mask[:-1]

        change_size_mask = np.full(delta_grid.shape, False)
        change_size_mask[1:] |= roll_right_mask
        change_size_mask[:-1] |= roll_left_mask

        change_idx = np.where(change_size_mask)[0]
        change_px = px_grid[change_idx]

        # options exists & delta doesn't change sign
        if change_px.shape[0] == 0:
            px_grid = np.zeros((1))
            px_grid[0] = under_px
            delta_grid = utils.get_portfolio_delta(fut_code, px_grid, utils.default_time_shift_strategy)

            if round(delta_grid[0]) == 0:
                if under_px < min_strike:
                    buy_px_grid = np.zeros(shape=(stops_num))
                    for idx in range(stops_num):
                        buy_px_grid[idx] = min_strike + config.get_config().STOP_PX_STEP * idx

                    delta_grid = utils.get_portfolio_delta(fut_code, buy_px_grid, utils.default_time_shift_strategy)
                    add_stop_orders(buy_px_grid, delta_grid)
                    set_order_sequence(np.linspace(0, stops_num - 1, stops_num, dtype=np.int32))

                elif under_px > max_strike:
                    sell_px_grid = np.zeros(shape=(stops_num))
                    for idx in range(stops_num):
                        sell_px_grid[idx] = max_strike - config.get_config().STOP_PX_STEP * idx

                    delta_grid = utils.get_portfolio_delta(fut_code, sell_px_grid, utils.default_time_shift_strategy)
                    add_stop_orders(sell_px_grid, delta_grid)
                    set_order_sequence(np.linspace(0, stops_num - 1, stops_num, dtype=np.int32))
                else:
                    exit(1)

            else:
                add_stop_orders(px_grid, delta_grid, order_type = 'MKT')
                set_order_sequence([0])
        # delta changes sign
        else:
            px_dist = np.abs(change_px - under_px)
            zero_delta_px_idx = np.argsort(px_dist)[0]
            zero_delta_px = change_px[zero_delta_px_idx]

            buy_px_grid = np.zeros(shape=(stops_num))
            for idx in range(stops_num):
                buy_px_grid[idx] = zero_delta_px + config.get_config().STOP_PX_STEP * (idx + 1)

            delta_grid = utils.get_portfolio_delta(fut_code, buy_px_grid, utils.default_time_shift_strategy)
            rounded_delta_grid = np.round(delta_grid)
            mask = rounded_delta_grid == 0
            if np.all(mask):
                right_strike_mask = strikes > zero_delta_px
                strikes_selection = strikes[right_strike_mask]
                if strikes_selection.shape[0] == 0:
                    exit(0)
                target_strike = np.min(strikes_selection)

                buy_px_grid = np.zeros(shape=(stops_num))
                for idx in range(stops_num):
                    buy_px_grid[idx] = target_strike + config.get_config().STOP_PX_STEP * idx

                delta_grid = utils.get_portfolio_delta(fut_code, buy_px_grid, utils.default_time_shift_strategy)
                add_stop_orders(buy_px_grid, delta_grid)
            else:
                add_stop_orders(buy_px_grid, delta_grid)

            stops_num = config.get_config().STOPS_NUM
            sell_px_grid = np.zeros(shape=(stops_num))
            for idx in range(stops_num):
                sell_px_grid[idx] = zero_delta_px - config.get_config().STOP_PX_STEP * (idx + 1)

            delta_grid = utils.get_portfolio_delta(fut_code, sell_px_grid, utils.default_time_shift_strategy)
            rounded_delta_grid = np.round(delta_grid)
            mask = rounded_delta_grid == 0
            if np.all(mask):
                left_strike_mask = strikes < zero_delta_px
                strikes_selection = strikes[left_strike_mask]
                if strikes_selection.shape[0] == 0:
                    exit(0)
                target_strike = np.max(strikes_selection)

                sell_px_grid = np.zeros(shape=(stops_num))
                for idx in range(stops_num):
                    sell_px_grid[idx] = target_strike - config.get_config().STOP_PX_STEP * idx

                delta_grid = utils.get_portfolio_delta(fut_code, sell_px_grid, utils.default_time_shift_strategy)
                add_stop_orders(sell_px_grid, delta_grid)
            else:
                add_stop_orders(sell_px_grid, delta_grid)

            orders_px_grid = np.concatenate((buy_px_grid, sell_px_grid))
            orders_zero_delta_px_distance_grid = np.abs(orders_px_grid - zero_delta_px)
            set_order_sequence(np.argsort(orders_zero_delta_px_distance_grid))

    return target_order_idx, target_code, target_qty, target_px, target_order_type
