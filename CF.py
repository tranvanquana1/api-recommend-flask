import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import read_data as rd
import json

X0 = rd.items.values
X_train_counts = X0[:, -19:]

category = np.array(['unknown ', 'Action ', 'Adventure ',
                     'Animation ', 'Children\'s ', 'Comedy ', 'Crime ', 'Documentary ', 'Drama ', 'Fantasy ',
                     'Film-Noir ', 'Horror ', 'Musical ', 'Mystery ', 'Romance ', 'Sci-Fi ', 'Thriller ', 'War ', 'Western'])


class CF(object):
    """docstring for CF"""

    def __init__(self, Y_data, k, dist_func=cosine_similarity, uuCF=1):
        self.uuCF = uuCF  # user-user (1) or item-item (0) CF
        self.Y_data = Y_data if uuCF else Y_data[:, [1, 0, 2]]
        self.k = k
        self.dist_func = dist_func
        self.Ybar_data = None
        # number of users and items. Remember to add 1 since id starts from 0
        self.n_users = int(np.max(self.Y_data[:, 1])) + 1
        self.n_items = int(np.max(self.Y_data[:, 0])) + 1

    def get_category(self, id):
        category_item = category.dot(X_train_counts[id]).strip()
        return category_item

    def add(self, new_data):
        """
        Update Y_data matrix when new ratings come.
        For simplicity, suppose that there is no new user or item.
        """

        self.Y_data = np.concatenate(
            (self.Y_data, np.matrix(new_data)[:, [1, 0, 2]]), axis=0)
        self.n_users = int(np.max(self.Y_data[:, 0])) + 1
        self.n_items = int(np.max(self.Y_data[:, 1])) + 1

        # convert to data frame
        table_ratings = pd.DataFrame(
            self.Y_data[:, [1, 0, 2]], columns=['user_id', 'movie_id', 'rating'])
        table_ratings.to_csv('ml-100k/u.data', index=False,
                             header=False, sep='\t', )

    def normalize_Y(self):
        items = self.Y_data[:, 0]  # all items - first col of the Y_data
        self.Ybar_data = self.Y_data.copy()
        self.mu = np.zeros((self.n_items,))
        for n in range(self.n_items):
            # row indices of rating for item n
            # since indices need to be integers, we need to convert
            ids = np.where(items == n)[0].astype(np.int32)
            # indices of all ratings for item n
            users_ids = self.Y_data[ids, 1]
            # and the corresponding ratings
            ratings = self.Y_data[ids, 2]
            # take mean
            m = np.mean(ratings)
            if np.isnan(m):
                m = 0  # to avoid empty array and nan value
            self.mu[n] = m
            # normalize
            self.Ybar_data[ids, 2] = ratings - self.mu[n]

        ################################################
        # form the rating matrix as a sparse matrix. Sparsity is important
        # for both memory and computing efficiency. For example, if #user = 1M,
        # #item = 100k, then shape of the rating matrix would be (1M, 100k),
        # you may not have enough memory to store this. Then, instead, we store
        # nonzeros only, and, of course, their locations.
        self.Ybar = sparse.coo_matrix((self.Ybar_data[:, 2],
                                       (self.Ybar_data[:, 1], self.Ybar_data[:, 0])), (self.n_users, self.n_items))
        self.Ybar = self.Ybar.tocsr()

    def similarity(self):
        eps = 1e-6
        self.S = self.dist_func(self.Ybar.T, self.Ybar.T)

    def refresh(self):
        """
        Normalize data and calculate similarity matrix again (after
        some few ratings added)
        """
        self.normalize_Y()
        self.similarity()

    def fit(self):
        self.refresh()

    def __pred(self, u, i, normalized=1):
        """
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        # Step 1: find all users who rated i
        ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
        # Step 2:
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
        # Step 3: find similarity btw the current user and others
        # who already rated i
        sim = self.S[u, users_rated_i]
        # Step 4: find the k most similarity users
        a = np.argsort(sim)[-self.k:]
        # and the corresponding similarity levels
        nearest_s = sim[a]
        # How did each of 'near' users rated item i
        r = self.Ybar[i, users_rated_i[a]]
        if normalized:
            # add a small number, for instance, 1e-8, to avoid dividing by 0
            return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8)

        return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8) + self.mu[u]

    def pred(self, u, i, normalized=1):
        """
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        if self.uuCF:
            return self.__pred(u, i, normalized)
        return self.__pred(i, u, normalized)

    def recommend(self, u):
        """
        Determine all items should be recommended for user u.
        The decision is made based on all i such that:
        self.pred(u, i) > 0. Suppose we are considering items which
        have not been rated by u yet.
        """
        ids = np.where(self.Y_data[:, 0] == u)[0]
        items_rated_by_u = self.Y_data[ids, 1].tolist()
        recommended_items = []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                rating = self.__pred(u, i)
                if rating > 0:
                    recommended_items.append(i)

        return recommended_items

    def recommend2(self, u, l):
        """
        Determine all items should be recommended for user u.
        The decision is made based on all i such that:
        self.pred(u, i) > 0. Suppose we are considering items which
        have not been rated by u yet.
        """
        print('total_user', u, l)

        if u < self.n_users:

            ids = np.where(self.Y_data[:, 1] == u)[0]

            # item indices rated by user_id
            items_rated_by_u = self.Y_data[ids, 1].tolist()
            recommended_items = []
            recommended_items_rating = []

            for i in range(self.n_items):
                if i not in items_rated_by_u:
                    rating = self.pred(u, i)
                    if rating > 0:
                        recommended_items.append(i)
                        recommended_items_rating.append(rating)

            recommended_items_rating = recommended_items_rating + self.mu[u]

            table_user_item = pd.DataFrame(
                {'movie_id': recommended_items,  'predict_rating': recommended_items_rating})

            # Sort theo predict rating
            table_sorted = table_user_item.head(l).sort_values(
                by='predict_rating', ascending=False)

            return table_sorted.values
        else:
            return []

    def print_recommendation(self):
        """
        print all items which should be recommended for each user
        """
        print('Recommendation: ')
        for u in range(self.n_users):
            recommended_items = self.recommend(u)
            if self.uuCF:
                print('    Recommend item(s):',
                      recommended_items, 'for user', u)
            else:
                print('    Recommend item', u,
                      'for user(s) : ', recommended_items)

    def print_recommendation_for_user(self, user):
        recommended_items = self.recommend2(user)
        if self.uuCF:
            print('    Recommend item(s):',
                  len(recommended_items), 'for user', user)
        else:
            print('    Recommend item', user,
                  'for user(s) : ', recommended_items)

        return recommended_items
