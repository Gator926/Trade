from unittest import TestCase
from CollectData.collect_data.Main import Main


class TestForMain(TestCase):
    def test_for_init_main_class(self):
        main = Main()
        self.assertEqual(main.name, "jack")