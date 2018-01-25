import numpy as np
import utils
import config

def main_levels_algo(fut_code, high, low, DELTA_TIME, last_px, buy_stps, sell_stps):
    # buy orders
    buy_orders_px = []
    buy_orders_delta = []

    current_px = high
    for p in buy_stps:
        SHIFT_PX, NUM, GRID_STEP_PX, FWD_PX, IS_SAFE = p

        if NUM == 0:
            continue

        #convert to real pxs
        SHIFT_PX = SHIFT_PX / config.get_config().FUT_PRICE_COEFF
        GRID_STEP_PX = GRID_STEP_PX / config.get_config().FUT_PRICE_COEFF
        FWD_PX = FWD_PX / config.get_config().FUT_PRICE_COEFF

        current_px += SHIFT_PX
        if IS_SAFE:
            current_px += GRID_STEP_PX

        stops_submitted = 0
        for _ in range(100):
            delta_px = current_px + FWD_PX
            stop_px = current_px
            delta = utils.get_portfolio_delta(fut_code, delta_px, utils.default_time_shift_strategy, DELTA_TIME)

            buy_orders_px.append(stop_px)
            buy_orders_delta.append(delta)
            stops_submitted += 1
            if stops_submitted >= NUM:
                break

            # if round(delta) < 0:
            #     buy_orders_px.append(stop_px)
            #     buy_orders_delta.append(delta)
            #     stops_submitted += 1
            #     if stops_submitted >= NUM:
            #         break
            current_px += GRID_STEP_PX
        current_px += FWD_PX

    # sell order
    sell_orders_px = []
    sell_orders_delta = []

    current_px = low
    for p in sell_stps:
        SHIFT_PX, NUM, GRID_STEP_PX, FWD_PX, IS_SAFE = p
        if NUM == 0:
            continue

        # convert to real pxs
        SHIFT_PX = SHIFT_PX / config.get_config().FUT_PRICE_COEFF
        GRID_STEP_PX = GRID_STEP_PX / config.get_config().FUT_PRICE_COEFF
        FWD_PX = FWD_PX / config.get_config().FUT_PRICE_COEFF

        current_px -= SHIFT_PX
        if IS_SAFE:
            current_px -= GRID_STEP_PX

        stops_submitted = 0
        for _ in range(100):
            delta_px = current_px - FWD_PX
            stop_px = current_px
            delta = utils.get_portfolio_delta(fut_code, delta_px, utils.default_time_shift_strategy, DELTA_TIME)

            sell_orders_px.append(stop_px)
            sell_orders_delta.append(delta)
            stops_submitted += 1
            if stops_submitted >= NUM:
                break



            # if round(delta) > 0:
            #     sell_orders_px.append(stop_px)
            #     sell_orders_delta.append(delta)
            #     stops_submitted += 1
            #     if stops_submitted >= NUM:
            #         break
            current_px -= GRID_STEP_PX
        current_px -= FWD_PX

    buy_orders_px_np = np.array(buy_orders_px)
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