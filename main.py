from CF import CF
import numpy as np
import pandas as pd
from datetime import datetime
import read_data as rd
import content_base_filter as cbf

from GoogleDriver import GoogleDriver


if __name__ == "__main__":

    gd = GoogleDriver()
    rate_train = gd.rate_train
    rate_train[:, :2] -= 1

    rs = CF(rate_train, k=30, uuCF=0)
    rs.fit()
    # print(rs.Y_data)
    # print(rs.n_users)
    # print(rs.n_items)
    # print('predict', rs.recommend2(942, 5))
