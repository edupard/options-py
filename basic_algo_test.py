import unittest
import utils
from basic_algo import basic_algo


class BasicAlgoTests(unittest.TestCase):

    def test_simple(self):
        # input this data & run test_simple by right click
        utils.parse_test_input("simple", "2018-01-22 13:11")

        target_order_idx, target_code, target_qty, target_px, target_order_type = basic_algo()

        # target_view_px = utils.convert_to_view_px_array(target_px)

        # self.assertEquals(target_qty, [158.0, 147.0, 128.0, -143.0, -129.0, -104.0])
        # self.assertEquals(target_view_px, ["122'110", "122'170", "122'230", "121'310", "121'250", "121'190"])
