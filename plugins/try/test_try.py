"Test for try plugin"
import pbt
import unittest

from unittest import mock

gctx = pbt.global_ctx
gctx.initial_setup()

class fakepip(object):
    def main():
        pass

class fakecode():
    def interact():
        pass

class fakeipython():
    def embed():
        pass

class TryTestCase(unittest.TestCase):

    def test_try_is_loaded(self):
        self.assertTrue(gctx.is_command("try"))

    def test_try_noipython(self):
        fakepip.main = mock.MagicMock()
        fakecode.interact= mock.MagicMock()
        with mock.patch.dict('sys.modules', {"pip": fakepip, "IPython": None,
                                             "code": fakecode}):
            gctx.run("try", ["requests"])
        # Can't Check on the call args because of the random folder
        self.assertTrue(fakepip.main.call_count==1)
        self.assertTrue(fakecode.interact.call_count==1)

    def test_try_ipython(self):
        fakepip.main = mock.MagicMock()
        fakecode.interact= mock.MagicMock()
        fakeipython.embed =  mock.MagicMock()
        with mock.patch.dict('sys.modules', {"pip": fakepip, "IPython": fakeipython,
                                             "code": fakecode}):
            gctx.run("try", ["requests"])
        # Can't Check on the call args because of the random folder
        self.assertTrue(fakepip.main.call_count==1)
        self.assertTrue(fakecode.interact.call_count==0)
        self.assertTrue(fakeipython.embed.call_count==1)


if __name__ == "__main__":
    unittest.main()
