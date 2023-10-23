import numpy as np
import pandas as pd

# implement k-means clustering algorithm

def kmeans(X, k, max_iter=900):
    """ k-means clustering algorithm
    Args:
        X: input data, shape: (n_samples, n_features)
        k: number of clusters
        max_iter: maximum number of iterations
    Returns:
        centroids: cluster centroids, shape: (k, n_features)
        labels: cluster labels for each data point, shape: (n_samples, )
    """
    # import pudb; pudb.set_trace()
    centroids = X[np.random.choice(X.shape[0], k, replace=False)]
    labels = np.zeros(X.shape[0])
    old_labels = None
    for _ in range(max_iter):
        # compute distances between each data point and each cluster centroid
        distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
        # assign each data point to the closest centroid
        labels = np.argmin(distances, axis=0)
        # update centroids
        centroids = update_centroids(X, labels, k)
        # no hay centroides con valores nullos o vac'ios
        assert np.isnan(centroids).any() == False
        # check if converged
        if old_labels is not None and np.array_equal(labels, old_labels):
            return centroids, labels
        old_labels = labels
    return centroids, labels

def update_centroids(X, labels, k):
    """ update centroids
        if there are not elements in a cluster, set the centroid to be the fartherst point from any cluster
    """
    centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])
    for i in range(k):
        if len(X[labels == i]) == 0:
            distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
            centroids[i] = X[np.argmax(distances[:, i])]
    return centroids


def concat_data_labels(df : pd.DataFrame, labels : np.ndarray):
    """ concatenate data and labels
    Args:
        df: input data, shape: (n_samples, n_features)
        labels: cluster labels for each data point, shape: (n_samples, )
    Returns:
        df: concatenated data and labels, shape: (n_samples, n_features + 1)
    """
    df_concatenated = df.copy()
    df_concatenated['label'] = labels
    return df_concatenated
def get_sorted_data(df : pd.DataFrame, label : int, point : np.ndarray):
    """ get data sorted by distance to a given point
    Args:
        df: input data, shape: (n_samples, n_features)
        label: cluster label
        point: given point, shape: (n_features, )
    Returns:
        df_sorted: sorted data, shape: (n_samples, n_features + 1)
    """
    df_sorted = df[df['label'] == label].copy()
    df_sorted['distance'] = np.sqrt(((df_sorted.drop(['name', 'label'], axis=1).values - point)**2).sum(axis=1))
    df_sorted = df_sorted.sort_values(by=['distance'], ascending=True)
    return df_sorted

def get_point_label_of_query(df : pd.DataFrame, query : str):
    """ get point and label of a given query
    Args:
        df: input data, shape: (n_samples, n_features)
        query: query name
    Returns:
        point: point of the query, shape: (n_features, )
        label: cluster label of the query
    """
    point = df[df['name'] == query].drop(['name', 'label'], axis=1).values[0]
    label = df[df['name'] == query]['label'].values[0]
    return point, label


def main(k=5):
    # import pudb; pudb.set_trace()
    # load data
    df = pd.read_csv('query_matrix.csv', index_col=0)
    X = df.drop(['name'], axis=1).values
    # run k-means clustering algorithm
    # import pudb; pudb.set_trace()
    centroids, labels = kmeans(X, k=k, max_iter=99999)
    # print results
    print('centroids:\n', centroids)
    print('labels:\n', labels)
    # concatenate data and labels
    df = concat_data_labels(df, labels)
    # get sorted data
    point, label = get_point_label_of_query(df, 'query')
    df_sorted = get_sorted_data(df, label, point)
    df_sorted = df_sorted[ df_sorted['label'] == label ]
    # save results
    df_sorted.to_csv('query_matrix_sorted.csv')
    df.to_csv('query_matrix_labeled.csv')
    # for a given cluster label in sorted order using euclidean distance





def test_setosa():
    import sklearn.datasets
    iris = sklearn.datasets.load_iris()
    X = iris.data
    y = iris.target
    centroids, labels = kmeans(X, k=3, max_iter=999)
    print('centroids:\n', centroids)
    print('labels:\n', labels)
    print('y:\n', y)


if __name__ == '__main__':
    main()
    print('test_setosa:')
    test_setosa()
