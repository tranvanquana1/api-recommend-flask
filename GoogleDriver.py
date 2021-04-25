# https://pythonhosted.org/PyDrive/quickstart.html
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

import pandas as pd
import numpy as np
import io
from datetime import datetime


class GoogleDriver(object):

    def __init__(self):

        # Below code does the authentication part of the code
        gauth = GoogleAuth()

        # Creates local webserver and auto handles authentication.
        gauth.LocalWebserverAuth()
        # Create GoogleDrive instance with authenticated GoogleAuth instance
        drive = GoogleDrive(gauth)

        # Initialize GoogleDriveFile instance with file id.

        self.file_id = '14uQ-7OrU5vMEVP0aoSJe5SJjzDfLTxqK'

        self.downloaded = drive.CreateFile({'id': self.file_id})
        self.csv_raw = io.StringIO(self.downloaded.GetContentString())

        self.r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

        self.ratings_base = pd.read_csv(
            self.csv_raw, sep=',', names=self.r_cols, encoding='latin-1', skiprows=[0], header=None)
        self.rate_train = self.ratings_base.values

    def get_content(self):
        return self.ratings_base

    def update_content(self, user_id, movie_id, rating):

        # current date and time
        now = datetime.now()
        timestamp = int(datetime.timestamp(now))

        data = self.downloaded.GetContentString()

        new_data = np.concatenate(
            (self.rate_train, np.matrix([[user_id, movie_id, rating, timestamp]])), axis=0)

        table_data = pd.DataFrame(
            new_data, columns=self.r_cols)

        data = str(table_data.to_csv(index=False))

        self.downloaded.SetContentString(data)
        self.downloaded.Upload()

        print('update complete')
