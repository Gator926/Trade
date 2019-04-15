from unittest import TestCase
from CollectData.collect_data.Gateio import GateWs
from CollectData.collect_data.Settings import Settings


class TestForGateio(TestCase):

    def test_init_class(self):
        """
        测试初始化类，检测是否能从setting中获取正确的配置信息
        :return:
        """
        gate_ws = GateWs(Settings['Gate']['url'], Settings['Gate']['secret_key'], Settings['Gate']['message'])
        self.assertEqual(gate_ws._GateWs__url, Settings['Gate']['url'])
        self.assertEqual(gate_ws._GateWs__api_key, Settings['Gate']['secret_key'])
        self.assertEqual(gate_ws._GateWs__secret_key, Settings['Gate']['message'])
