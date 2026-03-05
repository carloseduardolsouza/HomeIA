import pathlib
import sys
import os

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ["MLFLOW_ENABLED"] = "false"
