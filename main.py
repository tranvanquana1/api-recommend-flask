from CF import CF
import numpy as np
import pandas as pd
from datetime import datetime
import read_data as rd
import content_base_filter as cbf

from GoogleDriver import GoogleDriver


if __name__ == "__main__":

    gd = GoogleDriver()

    print(gd.rate_train)
