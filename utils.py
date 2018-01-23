import os
from optparse import OptionParser
import datetime
import pandas as pd
from py_vollib.black.greeks.analytical import delta as calc_delta
from py_vollib.black_scholes import black_scholes as black_scholes
import numpy as np
import config
import math

SECONDS_IN_DAY = 24 * 60 * 60


def convert_to_view_px(px):
    pxWhole = math.floor(px)
    pxPart = px - pxWhole
    pxPartConverted = round(pxPart * config.get_config().FUT_PRICE_COEFF)
    return "%.0f'%03.0f" % (pxWhole, pxPartConverted)


def convert_to_view_px_array(px_arr):
    return [convert_to_view_px(px) for px in px_arr]


def get_days(timedelta, year_days_count):
    return timedelta.total_seconds() / SECONDS_IN_DAY / year_days_count


def parse_test_input(DATA_FOLDER, S_TIME):
    # script folder
    SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))

    parser = OptionParser()
    (options, args) = parser.parse_args()

    RUN_TIME = datetime.datetime.strptime(S_TIME, '%Y-%m-%d %H:%M')

    POSITIONS_FILE = "%s\\test_data\\%s\\positions.csv" % (SCRIPT_FOLDER, DATA_FOLDER)
    TIME_BARS_FILE = "%s\\test_data\\%s\\time_bars.csv" % (SCRIPT_FOLDER, DATA_FOLDER)
    TARGET_ORDERS_FILE = "%s\\test_data\\%s\\target_orders.csv" % (SCRIPT_FOLDER, DATA_FOLDER)

    positions_df = pd.read_csv(POSITIONS_FILE)
    positions_df['Expiration'] = pd.to_datetime(positions_df.Expiry, format='%Y-%m-%d %H:%M')
    # hack
    # positions_df.Position = positions_df.Position * 100
    time_bars_df = pd.read_csv(TIME_BARS_FILE)
    time_bars_df['DateTime'] = pd.to_datetime(time_bars_df.Time, format='%Y-%m-%d %H:%M')

    config.get_config().RUN_TIME = RUN_TIME
    config.get_config().positions_df = positions_df
    config.get_config().time_bars_df = time_bars_df
    config.get_config().TARGET_ORDERS_FILE = TARGET_ORDERS_FILE


def parse_input():
    # script folder
    SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))

    parser = OptionParser()
    (options, args) = parser.parse_args()

    # сommand line arguments: data folder, time string
    DATA_FOLDER = args[0]
    S_TIME = args[1]
    RUN_TIME = datetime.datetime.strptime(S_TIME, '%Y-%m-%d %H:%M')
    if (len(args) >= 3):
        config.get_config().SCRIPT_PARAMS = args[2]

    if (len(args) >= 4):
        config.get_config().UPTREND = args[3] == "True"

    POSITIONS_FILE = "%s\\data\\%s\\positions.csv" % (SCRIPT_FOLDER, DATA_FOLDER)
    TIME_BARS_FILE = "%s\\data\\%s\\time_bars.csv" % (SCRIPT_FOLDER, DATA_FOLDER)
    TARGET_ORDERS_FILE = "%s\\data\\%s\\target_orders.csv" % (SCRIPT_FOLDER, DATA_FOLDER)

    positions_df = pd.read_csv(POSITIONS_FILE)
    positions_df['Expiration'] = pd.to_datetime(positions_df.Expiry, format='%Y-%m-%d %H:%M')
    # hack
    # positions_df.Position = positions_df.Position * 100
    time_bars_df = pd.read_csv(TIME_BARS_FILE)
    time_bars_df['DateTime'] = pd.to_datetime(time_bars_df.Time, format='%Y-%m-%d %H:%M')

    config.get_config().RUN_TIME = RUN_TIME
    config.get_config().positions_df = positions_df
    config.get_config().time_bars_df = time_bars_df
    config.get_config().TARGET_ORDERS_FILE = TARGET_ORDERS_FILE


def get_portfolio_params(fut_code, px_grid):
    positions_df = config.get_config().positions_df
    # initialize ret values
    delta_grid = np.zeros_like(px_grid)
    porfolio_px_grid = np.zeros_like(px_grid)
    porfolio_px_expiry_grid = np.zeros_like(px_grid)

    # get fut pos
    fut_df = positions_df[positions_df.Code == fut_code]
    fut_pos = 0
    fut_pos_px = 0
    fut_mult = 1000
    if (fut_df.shape[0] > 0):
        fut_row = fut_df.iloc[0]
        fut_pos = fut_row.Position
        fut_mult = fut_row.Multiplier
        fut_pos_px = fut_row.Price

    # get option position
    options_df = positions_df[positions_df.Underlying == fut_code]

    # iterate over all px in grid
    for F, idx in zip(px_grid, range(px_grid.shape[0])):
        delta = 0
        portfolio_px = 0
        portfolio_expiry_px = 0

        delta += fut_pos
        portfolio_px += fut_pos * F * fut_mult
        portfolio_expiry_px += fut_pos * F * fut_mult

        fut_premium = - fut_pos * fut_pos_px * fut_mult
        portfolio_px += fut_premium
        portfolio_expiry_px += fut_premium

        # iterate over all opt positions and calc portfolio params
        for index, row in options_df.iterrows():
            flag = 'c' if row.Right == 'Call' else 'p'
            K = row.Strike
            t = get_days(row.Expiration - config.get_config().RUN_TIME, config.get_config().YEAR_DAYS_COUNT)
            r = row.Ir / 100
            sigma = row.Vol / 100
            opt_pos = row.Position
            opt_mult = row.Multiplier
            pos_px = row.Price
            delta += calc_delta(flag, F, K, t, r, sigma) * opt_pos
            portfolio_px += black_scholes(flag, F, K, t, r, sigma) * opt_pos * opt_mult
            portfolio_expiry_px += black_scholes(flag, F, K, 0, r, sigma) * opt_pos * opt_mult

            opt_premium = - opt_pos * pos_px * opt_mult
            portfolio_px += opt_premium
            portfolio_expiry_px += opt_premium

        # store portfolio params
        delta_grid[idx] = delta
        porfolio_px_grid[idx] = portfolio_px
        porfolio_px_expiry_grid[idx] = portfolio_expiry_px

    return delta_grid, porfolio_px_grid, porfolio_px_expiry_grid


def default_time_shift_strategy(duration):
    if duration < datetime.timedelta(days=1):
        duration = datetime.timedelta(seconds=duration.total_seconds() / 2)
    elif duration < datetime.timedelta(days=2):
        duration_1 = datetime.timedelta(seconds=duration.total_seconds() / 2)
        duration_2 = duration - datetime.timedelta(days=1)
        duration = datetime.timedelta(seconds=(duration_1.total_seconds() + duration_2.total_seconds()) / 2)
    else:
        duration = duration - datetime.timedelta(days=1)
    return duration


def get_portfolio_delta(fut_code, px_grid, time_delta_strategy):
    positions_df = config.get_config().positions_df
    # initialize ret values
    delta_grid = np.zeros_like(px_grid)

    # get fut pos
    fut_df = positions_df[positions_df.Code == fut_code]
    fut_pos = 0
    if (fut_df.shape[0] > 0):
        fut_row = fut_df.iloc[0]
        fut_pos = fut_row.Position

    # get option position
    options_df = positions_df[positions_df.Underlying == fut_code]

    # iterate over all px in grid
    for F, idx in zip(px_grid, range(px_grid.shape[0])):
        delta = 0

        delta += fut_pos

        # iterate over all opt positions and calc portfolio params
        for index, row in options_df.iterrows():
            flag = 'c' if row.Right == 'Call' else 'p'
            K = row.Strike
            duration = row.Expiration - config.get_config().RUN_TIME
            duration = time_delta_strategy(duration)

            t = get_days(duration, config.get_config().YEAR_DAYS_COUNT)
            r = row.Ir / 100
            sigma = row.Vol / 100
            opt_pos = row.Position
            delta += calc_delta(flag, F, K, t, r, sigma) * opt_pos

        # store portfolio params
        delta_grid[idx] = delta

    return delta_grid


def get_fut_codes(positions_df):
    fut_codes_by_opt_pos = positions_df[positions_df.SecType == 'FOP'].Underlying.unique()
    fut_codes_by_fut_pos = positions_df[positions_df.SecType == 'FUT'].Code.unique()
    fut_codes = set(fut_codes_by_opt_pos).union(set(fut_codes_by_fut_pos))
    return fut_codes


def get_specific_bar(fut_code, hour, timedelta=datetime.timedelta(seconds=0), duration='4 hours'):
    time_bars_df = config.get_config().time_bars_df
    bar_time = config.get_config().RUN_TIME.replace(hour=19, minute=00)
    bar_time -= timedelta

    selection_df = time_bars_df[time_bars_df.DateTime == bar_time]
    if selection_df.shape[0] == 0:
        return None
    return selection_df.iloc[0]


def get_last_bar(fut_code, duration='4 hours'):
    time_bars_df = config.get_config().time_bars_df
    # sort all fut timebars
    sorted_bars = time_bars_df[(time_bars_df.Code == fut_code) & (time_bars_df.Length == duration)].sort_values(
        by='DateTime', ascending=False)
    # get last bar
    last_bar = sorted_bars.iloc[0]

    return last_bar


def add_stop_orders(fut_code, px_grid, delta_grid, order_type='STP'):
    closed_delta = 0
    for i in range(delta_grid.shape[0]):
        order_delta = round(-delta_grid[i] + closed_delta)
        closed_delta -= order_delta
        # create target order
        config.get_config().target_code.append(fut_code)
        config.get_config().target_qty.append(order_delta)
        config.get_config().target_px.append(px_grid[i])
        config.get_config().target_order_type.append(order_type)


_base_order_idx = 0


def set_order_sequence(order_idxs):
    global _base_order_idx
    for order_idx in order_idxs:
        config.get_config().target_order_idx.append(_base_order_idx + order_idx)
    _base_order_idx += order_idxs.shape[0]
