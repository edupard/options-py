import numpy as np
import utils
import config
import datetime


def algo_night_stops():
    stops_num = config.get_config().STOPS_NUM_BASIC

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        # specific bar
        # last_bar = utils.get_specific_bar(fut_code, hour=23, timedelta=datetime.timedelta(days=1))
        # get undelying px
        last_bar = utils.get_last_bar(fut_code)
        if last_bar.DateTime.hour != 23:
            exit(1)

        under_px = last_bar.Close

        if config.get_config().UPTREND:
            config.get_config().STOPS_NUM_NIGHT_SELL = 0
        else:
            config.get_config().STOPS_NUM_NIGHT_BUY = 0

        # basic stops on buy + safe stops on buy
        buy_px_grid = np.zeros(
            shape=(config.get_config().STOPS_NUM_NIGHT_BUY + config.get_config().STOPS_NUM_NIGHT_SAFE_BUY))
        delta_buy_px_grid = np.zeros(
            shape=(config.get_config().STOPS_NUM_NIGHT_BUY + + config.get_config().STOPS_NUM_NIGHT_SAFE_BUY))

        for idx in range(config.get_config().STOPS_NUM_NIGHT_BUY):
            buy_px_grid[idx] = under_px + config.get_config().STOP_PX_STEP_NIGHT_BUY * (idx + 1)
            delta_buy_px_grid[idx] = under_px + config.get_config().STOP_PX_STEP_NIGHT_BUY * (
                    idx + 1) + config.get_config().STOP_PX_STEP_NIGHT_FWD_BUY

        last_zero_delta_px = delta_buy_px_grid[
            config.get_config().STOPS_NUM_NIGHT_BUY - 1] if config.get_config().STOPS_NUM_NIGHT_BUY != 0 else under_px
        for idx in range(config.get_config().STOPS_NUM_NIGHT_SAFE_BUY):
            buy_px_grid[
                config.get_config().STOPS_NUM_NIGHT_BUY + idx] = last_zero_delta_px + config.get_config().STOP_PX_STEP_NIGHT_SAFE_BUY * (
                    idx + 1)
            delta_buy_px_grid[
                config.get_config().STOPS_NUM_NIGHT_BUY + idx] = last_zero_delta_px + config.get_config().STOP_PX_STEP_NIGHT_SAFE_BUY * (
                    idx + 1)

        delta_grid = utils.get_portfolio_delta(fut_code, delta_buy_px_grid, utils.default_time_shift_strategy)
        utils.add_stop_orders(fut_code, buy_px_grid, delta_grid)

        # basic stops on sell + safe stops on sell
        sell_px_grid = np.zeros(
            shape=(config.get_config().STOPS_NUM_NIGHT_SELL + config.get_config().STOPS_NUM_NIGHT_SAFE_SELL))
        delta_sell_px_grid = np.zeros(
            shape=(config.get_config().STOPS_NUM_NIGHT_SELL + + config.get_config().STOPS_NUM_NIGHT_SAFE_SELL))

        for idx in range(config.get_config().STOPS_NUM_NIGHT_SELL):
            sell_px_grid[idx] = under_px - config.get_config().STOP_PX_STEP_NIGHT_SELL * (idx + 1)
            delta_sell_px_grid[idx] = under_px - config.get_config().STOP_PX_STEP_NIGHT_SELL * (
                    idx + 1) - config.get_config().STOP_PX_STEP_NIGHT_FWD_SELL

        last_zero_delta_px = delta_sell_px_grid[
            config.get_config().STOPS_NUM_NIGHT_SELL - 1] if config.get_config().STOPS_NUM_NIGHT_SELL != 0 else under_px
        for idx in range(config.get_config().STOPS_NUM_NIGHT_SAFE_SELL):
            sell_px_grid[
                config.get_config().STOPS_NUM_NIGHT_SELL + idx] = last_zero_delta_px - config.get_config().STOP_PX_STEP_NIGHT_SAFE_SELL * (
                    idx + 1)
            delta_sell_px_grid[
                config.get_config().STOPS_NUM_NIGHT_SELL + idx] = last_zero_delta_px - config.get_config().STOP_PX_STEP_NIGHT_SAFE_SELL * (
                    idx + 1)

        delta_grid = utils.get_portfolio_delta(fut_code, delta_sell_px_grid, utils.default_time_shift_strategy)
        utils.add_stop_orders(fut_code, sell_px_grid, delta_grid)

        orders_px_grid = np.concatenate((buy_px_grid, sell_px_grid))
        orders_zero_delta_px_distance_grid = np.abs(orders_px_grid - under_px)
        num_orders = orders_zero_delta_px_distance_grid.shape[0]
        order_idxs = np.zeros(num_orders, dtype=np.int32)
        for order_idx, idx in zip(range(num_orders), np.argsort(orders_zero_delta_px_distance_grid)):
            order_idxs[idx] = order_idx
        utils.set_order_sequence(order_idxs)
