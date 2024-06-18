from .config import INSTALLED_APPS, MODEL_FILE_NAME
import importlib

for app in INSTALLED_APPS:
    try:
        importlib.import_module(f'{app}.{MODEL_FILE_NAME[:-3]}')
    except ModuleNotFoundError as e:
        print(e)
        continue