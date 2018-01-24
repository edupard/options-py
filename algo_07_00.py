import numpy as np
import utils
import config
import datetime


def algo_07_00():
    # shift time
    DELTA_TIME = config.get_config().RUN_TIME.replace(hour=7, minute=0, second=0, microsecond=0)

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        first_bar = utils.get_specific_bar(fut_code, hour=config.get_config().ALGO_07_00_FIRST_BAR_START_HOUR)
        second_bar = utils.get_specific_bar(fut_code, hour=config.get_config().ALGO_07_00_SECOND_BAR_START_HOUR)

        high = max(first_bar.High, second_bar.High)
        low = min(first_bar.Low, second_bar.Low)

        last_bar = utils.get_last_bar(fut_code)
        last_px = last_bar.Close

        # buy orders
        current_px = high + config.get_config().ALGO_07_00_BUY_ROOM
        buy_orders_px = []
        buy_orders_delta = []

        # main buy cycle
        main_stops_submitted = 0
        for _ in range(100):
            delta = utils.get_portfolio_delta(fut_code, current_px + config.get_config().ALGO_07_00_BUY_FWD, utils.default_time_shift_strategy, DELTA_TIME)
            if round(delta) < 0:
                buy_orders_px.append(current_px)
                buy_orders_delta.append(delta)
                main_stops_submitted += 1
            if main_stops_submitted >= config.get_config().ALGO_07_00_MAIN_BUY_STOPS:
                break
            current_px += config.get_config().ALGO_07_00_BUY_MAIN_STEP

        # safe buy cycle
        current_px += config.get_config().ALGO_07_00_BUY_FWD
        current_px += config.get_config().ALGO_07_00_BUY_SAFE_STEP
        safe_stops_submitted = 0
        for _ in range(100):
            delta = utils.get_portfolio_delta(fut_code, current_px, utils.default_time_shift_strategy, DELTA_TIME)
            if round(delta) < 0:
                buy_orders_px.append(current_px)
                buy_orders_delta.append(delta)
                safe_stops_submitted += 1

            if safe_stops_submitted >= config.get_config().ALGO_07_00_SAFE_BUY_STOPS:
                break
            current_px += config.get_config().ALGO_07_00_BUY_SAFE_STEP

        # sell orders
        current_px = low - config.get_config().ALGO_07_00_SELL_ROOM
        sell_orders_px = []
        sell_orders_delta = []

        # main buy cycle
        main_stops_submitted = 0
        for _ in range(100):
            if (current_px - config.get_config().ALGO_07_00_SELL_FWD) <= 0:
                break
            delta = utils.get_portfolio_delta(fut_code, current_px - config.get_config().ALGO_07_00_SELL_FWD,
                                              utils.default_time_shift_strategy, DELTA_TIME)
            if round(delta) > 0:
                sell_orders_px.append(current_px)
                sell_orders_delta.append(delta)
                main_stops_submitted += 1
            if main_stops_submitted >= config.get_config().ALGO_07_00_MAIN_SELL_STOPS:
                break
            current_px -= config.get_config().ALGO_07_00_SELL_MAIN_STEP

        # safe sell cycle
        current_px -= config.get_config().ALGO_07_00_SELL_FWD
        current_px -= config.get_config().ALGO_07_00_SELL_SAFE_STEP
        safe_stops_submitted = 0
        for _ in range(100):
            if current_px <= 0:
                break
            delta = utils.get_portfolio_delta(fut_code, current_px, utils.default_time_shift_strategy, DELTA_TIME)
            if round(delta) > 0:
                sell_orders_px.append(current_px)
                sell_orders_delta.append(delta)
                safe_stops_submitted += 1

            if safe_stops_submitted >= config.get_config().ALGO_07_00_SAFE_SELL_STOPS:
                break
            current_px -= config.get_config().ALGO_07_00_SELL_SAFE_STEP

        buy_orders_px_np =  np.array(buy_orders_px)
        buy_orders_px_delta_np = np.array(buy_orders_delta)

        sell_orders_px_np = np.array(sell_orders_px)
        sell_orders_delta_np = np.array(sell_orders_delta)

        utils.add_stop_orders(fut_code, buy_orders_px_np, buy_orders_px_delta_np)
        utils.add_stop_orders(fut_code, sell_orders_px_np, sell_orders_delta_np)

        orders_px_grid = np.concatenate((buy_orders_px_np, sell_orders_px_np))
        orders_distance_grid = np.abs(orders_px_grid - last_px)
        num_orders = orders_distance_grid.shape[0]
        order_idxs = np.zeros(num_orders, dtype=np.int32)
        for order_idx, idx in zip(range(num_orders), np.argsort(orders_distance_grid)):
            order_idxs[idx] = order_idx
        utils.set_order_sequence(order_idxs)
