import unittest

if __name__ == '__main__':
    # Automatically discover all tests in the same directory as this script
    # and in any subdirectories under it, matching the pattern '*test.py'
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='*test.py')
    
    # Run the discovered tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
