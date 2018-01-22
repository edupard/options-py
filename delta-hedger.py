import pandas as pd


import utils
import config

from basic_algo import basic_algo
from algo_23_00 import algo_23_00

utils.parse_input()


if config.get_config().SCRIPT_PARAMS == "BASIC":
    target_order_idx, target_code, target_qty, target_px, target_order_type = basic_algo()
elif config.get_config().SCRIPT_PARAMS == "23_00":
    target_order_idx, target_code, target_qty, target_px, target_order_type = algo_23_00()

target_orders_df = pd.DataFrame({
    'idx' : target_order_idx,
    'code': target_code,
    'qty': target_qty,
    'px': target_px,
    'view_px' : utils.convert_to_view_px_array(target_px),
    'type': target_order_type
})

target_orders_df.to_csv(config.get_config().TARGET_ORDERS_FILE,index=False)
