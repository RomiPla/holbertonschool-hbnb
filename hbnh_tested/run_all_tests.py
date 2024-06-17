#!/usr/bin/python3
import unittest
import os

def run_tests():
    start_dir = os.path.dirname(__file__)
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir, pattern='test*.py')
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    if run_tests():
        print("Todas las pruebas pasaron correctamente.")
    else:
        print("Algunas pruebas fallaron.")
