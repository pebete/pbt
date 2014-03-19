"""test for helloworld plugin"""
import sys
sys.path.append("src")
import pbt
import unittest

gctx = pbt.global_ctx

class HelloWorldTestCase(unittest.TestCase):

    def test_plugin_is_loaded(self):
        gctx.initial_setup()
        self.assertTrue(gctx.is_command("hello"))
