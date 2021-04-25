from sklearn import linear_model
from sklearn.linear_model import Ridge
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import math
import numpy as np
import pickle
import json

import read_data as rd


X0 = rd.items.values
X_train_counts = X0[:, -19:]

category = np.array(['unknown ', 'Action ', 'Adventure ',
                     'Animation ', 'Children\'s ', 'Comedy ', 'Crime ', 'Documentary ', 'Drama ', 'Fantasy ',
                     'Film-Noir ', 'Horror ', 'Musical ', 'Mystery ', 'Romance ', 'Sci-Fi ', 'Thriller ', 'War ', 'Western'])

# lấy thể loại phim


def get_category(id):
    category_item = category.dot(X_train_counts[id]).strip()
    return category_item


# tfidf
transformer = TfidfTransformer(smooth_idf=True, norm='l2')
tfidf = transformer.fit_transform(X_train_counts.tolist()).toarray()

# print(tfidf[[0, 1, 2, 3, 4], :])


def get_items_rated_by_user(rate_matrix, user_id):
    """
    in each line of rate_matrix, we have infor: user_id, item_id, rating (scores), time_stamp
    we care about the first three values
    return (item_ids, scores) rated by user user_id
    """
    y = rate_matrix[:, 0]  # all users
    # item indices rated by user_id
    # we need to +1 to user_id since in the rate_matrix, id starts from 1
    # while index in python starts from 0
    ids = np.where(y == user_id + 1)[0]
    item_ids = rate_matrix[ids, 1] - 1  # index starts from 0
    scores = rate_matrix[ids, 2]
    return (item_ids, scores)

# train model cho tung user


filename = 'models/user_model_'


def trainModel():
    # Tìm mô hình cho mỗi user
    d = tfidf.shape[1]  # data dimension
    W = np.zeros((d, rd.n_users))
    b = np.zeros((1, rd.n_users))

    for n in range(rd.n_users):
        ids, scores = get_items_rated_by_user(rd.rate_train, n)
        clf = Ridge(alpha=0.01, fit_intercept=True)
        Xhat = tfidf[ids, :]

        clf.fit(Xhat, scores)

        # lưu model
        tuple_objects = (clf, Xhat, scores)
        pickle.dump(tuple_objects, open(filename + str(n+1) + '.pkl', 'wb'))

        W[:, n] = clf.coef_
        b[0, n] = clf.intercept_


def precision(user_id):
    ids, ratings = get_items_rated_by_user(rd.rate_test, user_id-1)

    movie_title = rd.items.values[:, 1]
    release_date = rd.items.values[:, 2]
    IMDb_URL = rd.items.values[:, 4]
    category_list = get_category(X0[:, 0]-1)

    # print('user_id:', user_id)

    pickled_model, pickled_Xhat, pickled_scores = pickle.load(
        open(filename + str(user_id) + '.pkl', 'rb'))

    predict = pickled_model.predict(tfidf[:, :])

    # print('predict:', pickled_scores)

    # hiển thị theo dataframe pandas
    table_user_item = pd.DataFrame(
        {'movie_id': X0[:, 0], "movie_title": movie_title, "release_date": release_date, "IMDb_URL": IMDb_URL, 'category': category_list, 'predict_rating': predict})

    # Sort theo predict rating
    table_sorted = table_user_item.sort_values(
        by='predict_rating', ascending=False)

    result = table_sorted.head(10).to_json(orient='records')
    parsed = json.loads(result)

    return json.dumps(parsed, indent=2)


def evaluate(Yhat, rates, W, b):
    se = 0
    cnt = 0
    for n in xrange(n_users):
        ids, scores_truth = get_items_rated_by_user(rates, n)
        scores_pred = Yhat[ids, n]
        e = scores_truth - scores_pred
        se += (e*e).sum(axis=0)
        cnt += e.size
    return sqrt(se/cnt)


if __name__ == '__main__':
    print('predict---------------------------')
    # print(precision(10))
    print(get_category(10))
