import sys
from pathlib import Path

module_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(module_dir))
