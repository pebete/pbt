import pbt
import sys
import unittest

@pbt.command(name="test")
def run(ctx, args, project):
    loader = unittest.TestLoader()
    for test_dir in project.settings.test_paths:
        tests = loader.discover(test_dir)
        testRunner = unittest.runner.TextTestRunner()
        testRunner.run(tests)

