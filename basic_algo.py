import numpy as np
import utils
import config


def basic_algo():
    stops_num = config.get_config().STOPS_NUM_BASIC


    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:

        # get undelying px
        last_bar = utils.get_last_bar(fut_code)
        under_px = last_bar.Close

        strikes = positions_df[positions_df.Underlying == fut_code].Strike.values
        #only futures in position
        if strikes.shape[0] == 0:
            # push delta hedging order
            px_grid = np.zeros((1))
            px_grid[0] = under_px
            delta_grid = utils.get_portfolio_delta(fut_code, px_grid, utils.default_time_shift_strategy)
            utils.add_stop_orders(fut_code, px_grid, delta_grid, order_type='MKT')
            utils.set_order_sequence(np.array([0]))
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

            # delta is zero at current price
            if round(delta_grid[0]) == 0:
                if under_px < min_strike:
                    buy_px_grid = np.zeros(shape=(stops_num))
                    for idx in range(stops_num):
                        buy_px_grid[idx] = min_strike + config.get_config().STOP_PX_STEP_BASIC * idx

                    delta_grid = utils.get_portfolio_delta(fut_code, buy_px_grid, utils.default_time_shift_strategy)
                    utils.add_stop_orders(fut_code, buy_px_grid, delta_grid)
                    utils.set_order_sequence(np.linspace(0, stops_num - 1, stops_num, dtype=np.int32))

                elif under_px > max_strike:
                    sell_px_grid = np.zeros(shape=(stops_num))
                    for idx in range(stops_num):
                        sell_px_grid[idx] = max_strike - config.get_config().STOP_PX_STEP_BASIC * idx

                    delta_grid = utils.get_portfolio_delta(fut_code, sell_px_grid, utils.default_time_shift_strategy)
                    utils.add_stop_orders(fut_code, sell_px_grid, delta_grid)
                    utils.set_order_sequence(np.linspace(0, stops_num - 1, stops_num, dtype=np.int32))
                else:
                    right_strike_mask = strikes >= under_px
                    strikes_selection = strikes[right_strike_mask]
                    if strikes_selection.shape[0] == 0:
                        exit(0)
                    target_strike = np.min(strikes_selection)

                    buy_px_grid = np.zeros(shape=(stops_num))
                    for idx in range(stops_num):
                        buy_px_grid[idx] = target_strike + config.get_config().STOP_PX_STEP_BASIC * idx

                    delta_grid = utils.get_portfolio_delta(fut_code, buy_px_grid, utils.default_time_shift_strategy)
                    utils.add_stop_orders(fut_code, buy_px_grid, delta_grid)

                    left_strike_mask = strikes <= under_px
                    strikes_selection = strikes[left_strike_mask]
                    if strikes_selection.shape[0] == 0:
                        exit(0)
                    target_strike = np.max(strikes_selection)

                    sell_px_grid = np.zeros(shape=(stops_num))
                    for idx in range(stops_num):
                        sell_px_grid[idx] = target_strike - config.get_config().STOP_PX_STEP_BASIC * idx

                    delta_grid = utils.get_portfolio_delta(fut_code, sell_px_grid, utils.default_time_shift_strategy)
                    utils.add_stop_orders(fut_code, sell_px_grid, delta_grid)

                    orders_px_grid = np.concatenate((buy_px_grid, sell_px_grid))
                    orders_zero_delta_px_distance_grid = np.abs(orders_px_grid - under_px)
                    num_orders = orders_zero_delta_px_distance_grid.shape[0]
                    order_idxs = np.zeros(num_orders, dtype=np.int32)
                    for order_idx, idx in zip(range(num_orders), np.argsort(orders_zero_delta_px_distance_grid)):
                        order_idxs[idx] = order_idx
                        utils.set_order_sequence(order_idxs)
            # place market stop
            else:
                utils.add_stop_orders(fut_code, px_grid, delta_grid, order_type='MKT')
                utils.set_order_sequence(np.array([0]))
        # delta changes sign
        else:
            px_dist = np.abs(change_px - under_px)
            zero_delta_px_idx = np.argsort(px_dist)[0]
            zero_delta_px = change_px[zero_delta_px_idx]

            buy_px_grid = np.zeros(shape=(stops_num))
            for idx in range(stops_num):
                buy_px_grid[idx] = zero_delta_px + config.get_config().STOP_PX_STEP_BASIC * (idx + 1)

            delta_grid = utils.get_portfolio_delta(fut_code, buy_px_grid, utils.default_time_shift_strategy)
            rounded_delta_grid = np.round(delta_grid)
            mask = rounded_delta_grid == 0
            # all buy stops are zero
            if np.all(mask):
                right_strike_mask = strikes > zero_delta_px
                strikes_selection = strikes[right_strike_mask]
                if strikes_selection.shape[0] == 0:
                    exit(0)
                target_strike = np.min(strikes_selection)

                buy_px_grid = np.zeros(shape=(stops_num))
                for idx in range(stops_num):
                    buy_px_grid[idx] = target_strike + config.get_config().STOP_PX_STEP_BASIC * idx

                delta_grid = utils.get_portfolio_delta(fut_code, buy_px_grid, utils.default_time_shift_strategy)
                utils.add_stop_orders(fut_code, buy_px_grid, delta_grid)
            else:
                utils.add_stop_orders(fut_code, buy_px_grid, delta_grid)

            stops_num = config.get_config().STOPS_NUM_BASIC
            sell_px_grid = np.zeros(shape=(stops_num))
            for idx in range(stops_num):
                sell_px_grid[idx] = zero_delta_px - config.get_config().STOP_PX_STEP_BASIC * (idx + 1)

            delta_grid = utils.get_portfolio_delta(fut_code, sell_px_grid, utils.default_time_shift_strategy)
            rounded_delta_grid = np.round(delta_grid)
            mask = rounded_delta_grid == 0
            # all sell stops are zero
            if np.all(mask):
                left_strike_mask = strikes < zero_delta_px
                strikes_selection = strikes[left_strike_mask]
                if strikes_selection.shape[0] == 0:
                    exit(0)
                target_strike = np.max(strikes_selection)

                sell_px_grid = np.zeros(shape=(stops_num))
                for idx in range(stops_num):
                    sell_px_grid[idx] = target_strike - config.get_config().STOP_PX_STEP_BASIC * idx

                delta_grid = utils.get_portfolio_delta(fut_code, sell_px_grid, utils.default_time_shift_strategy)
                utils.add_stop_orders(fut_code, sell_px_grid, delta_grid)
            else:
                utils.add_stop_orders(fut_code, sell_px_grid, delta_grid)

            orders_px_grid = np.concatenate((buy_px_grid, sell_px_grid))
            orders_zero_delta_px_distance_grid = np.abs(orders_px_grid - zero_delta_px)
            num_orders = orders_zero_delta_px_distance_grid.shape[0]
            order_idxs = np.zeros(num_orders, dtype=np.int32)
            for order_idx, idx in zip(range(num_orders), np.argsort(orders_zero_delta_px_distance_grid)):
                order_idxs[idx] = order_idx
            utils.set_order_sequence(order_idxs)
