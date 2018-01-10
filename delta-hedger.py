import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import utils
import config

utils.parse_input()

target_orders = []
target_code = []
target_qty = []
target_px = []

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
    under_px =last_bar.Close

    lower_px = max(under_px - config.get_config().GRID_PX_STEP * config.get_config().PROFILE_STEPS, 0)
    upper_px = under_px + config.get_config().GRID_PX_STEP * config.get_config().PROFILE_STEPS
    px_grid =np.linspace(lower_px, upper_px, num=(upper_px - lower_px) // config.get_config().GRID_PX_STEP + 1)

    delta_grid, porfolio_px_grid, porfolio_px_expiry_grid = utils.get_portfolio_params(fut_code, px_grid)

    # plot portfolio profile
    min_px = min(np.min(porfolio_px_grid), np.min(porfolio_px_expiry_grid))
    max_px = max(np.max(porfolio_px_grid), np.max(porfolio_px_expiry_grid))
    curr_px_line_x = np.array([under_px, under_px])
    curr_px_line_y = np.array([min_px, max_px])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(px_grid, porfolio_px_grid, 'r-')
    ax.plot(px_grid, porfolio_px_expiry_grid, 'bo')
    ax.plot(curr_px_line_x, curr_px_line_y, 'g--')
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%0.0f'))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%0.3f'))
    ax.grid(True, linestyle='-', color='0.75')

plt.show(True)

target_orders_df = pd.DataFrame({
    'code': target_code,
    'qty': target_qty,
    'px': target_px,
})

target_orders_df.to_csv(config.get_config().TARGET_ORDERS_FILE,index=False)