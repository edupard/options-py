import pandas as pd


import utils
import config

from basic_algo import basic_algo
from algo_close_delta import algo_close_delta
from algo_close_delta_15_00 import algo_close_delta_15_00
from algo_night import algo_night
from algo_07_00 import algo_07_00
from algo_news import algo_news
from algo_stat import algo_stat
from algo_19_00 import algo_19_00
from algo_11_00 import algo_11_00
from algo_safe import algo_safe

utils.parse_input()


if config.get_config().SCRIPT_PARAMS == "BASIC":
    basic_algo()
elif config.get_config().SCRIPT_PARAMS == "CLOSE_DELTA":
    algo_close_delta()
elif config.get_config().SCRIPT_PARAMS == "CLOSE_DELTA_15_00":
    algo_close_delta_15_00()
elif config.get_config().SCRIPT_PARAMS == "NIGHT":
    algo_night()
elif config.get_config().SCRIPT_PARAMS == "07_00":
    algo_07_00()
elif config.get_config().SCRIPT_PARAMS == "11_00":
    algo_11_00()
elif config.get_config().SCRIPT_PARAMS == "NEWS":
    algo_news()
elif config.get_config().SCRIPT_PARAMS == "STAT":
    algo_stat()
elif config.get_config().SCRIPT_PARAMS == "19_00":
    algo_19_00()
elif config.get_config().SCRIPT_PARAMS == "EMPTY":
    _todo = 0
elif config.get_config().SCRIPT_PARAMS == "SAFE":
    algo_safe()

target_orders_df = pd.DataFrame({
    'idx' : config.get_config().target_order_idx,
    'code': config.get_config().target_code,
    'qty': config.get_config().target_qty,
    'px': config.get_config().target_px,
    'view_px' : utils.convert_to_view_px_array(config.get_config().target_px),
    'type': config.get_config().target_order_type
})

target_orders_df.to_csv(config.get_config().TARGET_ORDERS_FILE,index=False)
