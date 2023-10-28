import os, pathlib
import pytest

os.environ['STORAGE_PATH'] = 'test_storage/'

os.chdir( pathlib.Path.cwd() / 'tests' )

pytest.main()