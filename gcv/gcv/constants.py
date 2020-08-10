import os
from pathlib import Path
BASEDIR = Path(__file__).parent.parent.resolve()
RUNNING_WINDOWS = os.name == 'nt'
__all__ = ['BASEDIR', 'RUNNING_WINDOWS']
