from CF import CF
import numpy as np
import pandas as pd
from datetime import datetime

from GoogleDriver import GoogleDriver


if __name__ == "__main__":
    gd = GoogleDriver()

    print(gd.get_content())
