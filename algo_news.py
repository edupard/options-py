import utils
import config

from main_levels_algo import main_levels_algo

def algo_news():
    # shift time
    DELTA_TIME = config.get_config().RUN_TIME.replace(hour=15, minute=0, second=0, microsecond=0)

    # find all futures
    positions_df = config.get_config().positions_df
    time_bars_df = config.get_config().time_bars_df

    fut_codes = utils.get_fut_codes(positions_df)

    for fut_code in fut_codes:
        BAR_4H_S_H, BAR_4H_S_M = config.get_config().ALGO_NEWS_4H_BAR
        bar_4h = utils.get_specific_bar(fut_code, hour=BAR_4H_S_H, minute=BAR_4H_S_M)

        M5_S_H, M5_S_M, M5_E_H, M5_E_M =  config.get_config().ALGO_NEWS_5M_RANGE
        bars_5_min = utils.get_bars_range(fut_code,
                                          start_hour=M5_S_H,
                                          start_minute=M5_S_M,
                                          end_hour=M5_E_H,
                                          end_minute=M5_E_M,
                                          duration='5 mins',
                                          )
        M1_S_H, M1_S_M, M1_E_H, M1_E_M = config.get_config().ALGO_NEWS_1M_RANGE
        bars_1_min = utils.get_bars_range(fut_code,
                                          start_hour=M1_S_H,
                                          start_minute=M1_S_M,
                                          end_hour=M1_E_H,
                                          end_minute=M1_E_M,
                                          duration='1 min',
                                          )

        second_bar_open = bars_5_min.iloc[0].Open
        second_bar_close= bars_1_min.iloc[-1].Close
        second_bar_high = second_bar_open
        second_bar_low = second_bar_open
        for _, bar in bars_5_min.iterrows():
            second_bar_high = max(second_bar_high, bar.High)
        for _, bar in bars_1_min.iterrows():
            second_bar_high = max(second_bar_high, bar.High)

        for _, bar in bars_5_min.iterrows():
            second_bar_low = max(second_bar_low, bar.Low)
        for _, bar in bars_1_min.iterrows():
            second_bar_low = max(second_bar_low, bar.Low)


        if bar_4h.Close > bar_4h.Open:
            high = max(bar_4h.High, second_bar_high)
            low = min(bar_4h.Open, second_bar_low)
        elif bar_4h.Close < bar_4h.Open:
            high = max(bar_4h.Open, second_bar_high)
            low = min(bar_4h.Low, second_bar_low)
        else:
            high = max(bar_4h.High, second_bar_high)
            low = min(bar_4h.Low, second_bar_low)

        last_bar = utils.get_last_bar(fut_code)
        last_px = last_bar.Close

        buy_stps = config.get_config().ALGO_NEWS_BUY_STP
        sell_stps = config.get_config().ALGO_NEWS_SELL_STP

        # condition = False
        # if condition:
        #     config.get_config().ALGO_NEWS_BUY_STP = [
        #         (5, 1, 45, 45),
        #         (0, 2, 15, 15),
        #         (0, 3, 65, 0)
        #     ]

        main_levels_algo(fut_code, high, low, DELTA_TIME, last_px, buy_stps, sell_stps)
