import numpy as np
import utils
import config

class FwdLevelsAlgoParams(object):
    def __init__(self):
        self.BUY_ROOM = None
        self.BUY_FWD = None
        self.BUY_MAIN_STEP = None
        self.MAIN_BUY_ADD_STOPS = None
        self.BUY_ADD_FWD = None
        self.BUY_ADD_MAIN_STEP = None
        self.SAFE_BUY_STOPS = None
        self.BUY_SAFE_STEP = None
        self.SELL_ROOM = None
        self.SELL_FWD = None
        self.SELL_MAIN_STEP = None
        self.MAIN_SELL_ADD_STOPS = None
        self.SELL_ADD_FWD = None
        self.SELL_ADD_MAIN_STEP = None
        self.SAFE_SELL_STOPS = None
        self.SELL_SAFE_STE = None

def fwd_levels_algo(fut_code, high, low, DELTA_TIME, last_px, params):
    # buy orders
    current_px = high + params.BUY_ROOM
    buy_orders_px = []
    buy_orders_delta = []

    # first buy cycle
    for _ in range(100):
        delta = utils.get_portfolio_delta(fut_code, current_px + params.BUY_FWD,
                                          utils.default_time_shift_strategy, DELTA_TIME)
        if round(delta) < 0:
            buy_orders_px.append(current_px)
            buy_orders_delta.append(delta)
            break
        current_px += params.BUY_MAIN_STEP

    # additional buy cycle
    current_px += params.BUY_FWD
    main_stops_submitted = 0
    for _ in range(100):
        delta = utils.get_portfolio_delta(fut_code, current_px + params.BUY_ADD_FWD,
                                          utils.default_time_shift_strategy, DELTA_TIME)
        if round(delta) < 0:
            buy_orders_px.append(current_px)
            buy_orders_delta.append(delta)
            main_stops_submitted += 1
        if main_stops_submitted >= params.MAIN_BUY_ADD_STOPS:
            break
        current_px += params.BUY_ADD_MAIN_STEP

    # safe buy cycle
    current_px += params.BUY_ADD_FWD
    current_px += params.BUY_SAFE_STEP
    safe_stops_submitted = 0
    for _ in range(100):
        delta = utils.get_portfolio_delta(fut_code, current_px, utils.default_time_shift_strategy, DELTA_TIME)
        if round(delta) < 0:
            buy_orders_px.append(current_px)
            buy_orders_delta.append(delta)
            safe_stops_submitted += 1

        if safe_stops_submitted >= params.SAFE_BUY_STOPS:
            break
        current_px += params.BUY_SAFE_STEP

    # sell orders
    current_px = low - params.SELL_ROOM
    sell_orders_px = []
    sell_orders_delta = []

    # first sell cycle
    for _ in range(100):
        if (current_px - params.SELL_FWD) <= 0:
            break
        delta = utils.get_portfolio_delta(fut_code, current_px - params.SELL_FWD,
                                          utils.default_time_shift_strategy, DELTA_TIME)
        if round(delta) > 0:
            sell_orders_px.append(current_px)
            sell_orders_delta.append(delta)
            break
        current_px -= params.SELL_MAIN_STEP

    # additional sell cycle
    current_px -= params.SELL_FWD
    main_stops_submitted = 0
    for _ in range(100):
        if (current_px - params.SELL_ADD_FWD) <= 0:
            break
        delta = utils.get_portfolio_delta(fut_code, current_px - params.SELL_ADD_FWD,
                                          utils.default_time_shift_strategy, DELTA_TIME)
        if round(delta) > 0:
            sell_orders_px.append(current_px)
            sell_orders_delta.append(delta)
            main_stops_submitted += 1
        if main_stops_submitted >= params.MAIN_SELL_ADD_STOPS:
            break
        current_px -= params.SELL_ADD_MAIN_STEP

    # safe sell cycle
    current_px -= params.SELL_ADD_FWD
    current_px -= params.SELL_SAFE_STEP
    safe_stops_submitted = 0
    for _ in range(100):
        if current_px <= 0:
            break
        delta = utils.get_portfolio_delta(fut_code, current_px, utils.default_time_shift_strategy, DELTA_TIME)
        if round(delta) > 0:
            sell_orders_px.append(current_px)
            sell_orders_delta.append(delta)
            safe_stops_submitted += 1

        if safe_stops_submitted >= params.SAFE_SELL_STOPS:
            break
        current_px -= params.SELL_SAFE_STEP

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