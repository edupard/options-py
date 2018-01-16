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


def parse_input():
    # script folder
    SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))

    parser = OptionParser()
    (options, args) = parser.parse_args()

    # сommand line arguments: data folder, time string
    DATA_FOLDER = args[0]
    S_TIME = args[1]
    RUN_TIME = datetime.datetime.strptime(S_TIME, '%Y-%m-%d %H:%M')
    if (len(args) == 3):
        config.get_config().SCRIPT_PARAMS = args[2]

    POSITIONS_FILE = "%s\\data\\%s\\positions.csv" % (SCRIPT_FOLDER, DATA_FOLDER)
    TIME_BARS_FILE = "%s\\data\\%s\\time_bars.csv" % (SCRIPT_FOLDER, DATA_FOLDER)
    TARGET_ORDERS_FILE = "%s\\data\\%s\\target_orders.csv" % (SCRIPT_FOLDER, DATA_FOLDER)

    positions_df = pd.read_csv(POSITIONS_FILE)
    positions_df['Expiration'] = pd.to_datetime(positions_df.Expiry, format='%Y-%m-%d %H:%M')
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


def get_portfolio_delta(fut_code, px_grid):
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
            t = get_days(row.Expiration - config.get_config().RUN_TIME, config.get_config().YEAR_DAYS_COUNT)
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


def get_last_bar(fut_code, duration='4 hours'):
    time_bars_df = config.get_config().time_bars_df
    # sort all fut timebars
    sorted_bars = time_bars_df[(time_bars_df.Code == fut_code) & (time_bars_df.Length == duration)].sort_values(
        by='DateTime', ascending=False)
    # get last bar
    last_bar = sorted_bars.iloc[0]

    return last_bar
