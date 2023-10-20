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
    centroids = X[np.random.choice(X.shape[0], k, replace=False)]
    labels = np.zeros(X.shape[0])
    old_labels = None
    for _ in range(max_iter):
        # compute distances between each data point and each cluster centroid
        distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
        # assign each data point to the closest centroid
        labels = np.argmin(distances, axis=0)
        # update centroids
        centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])
        # check if converged
        if old_labels is not None and np.array_equal(labels, old_labels):
            return centroids, labels
        old_labels = labels
    return centroids, labels

def concat_data_and_labels(X, labels):
    """ concatenate data and labels
    Args:
        X: input data, shape: (n_samples, n_features)
        labels: cluster labels for each data point, shape: (n_samples, )
    Returns:
        data_and_labels: data and labels, shape: (n_samples, n_features+1)
    """
    data_and_labels = np.concatenate((X, labels[:, np.newaxis]), axis=1)
    return data_and_labels
def data_and_labels_to_df(data_and_labels):
    """ convert data and labels to dataframe
    Args:
        data_and_labels: data and labels, shape: (n_samples, n_features+1)
    Returns:
        df: dataframe
    """
    df = pd.DataFrame(data_and_labels)
    return df

def main():
    # load data
    df = pd.read_csv('query_matrix.csv', header=0)
    X = df.values
    # run k-means clustering algorithm
    # import pudb; pudb.set_trace()
    centroids, labels = kmeans(X, k=3, max_iter=99999)
    # print results
    print('centroids:\n', centroids)
    print('labels:\n', labels)
    # concatenate data and labels
    data_and_labels = concat_data_and_labels(X, labels)
    # convert data and labels to dataframe
    df = data_and_labels_to_df(data_and_labels)
    print('df:\n', df)
    # save results
    print('data_and_labels:\n', data_and_labels)



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
    # print('test_setosa:')
    # test_setosa()
