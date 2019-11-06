from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def kmeans_elbow_plot(df):
    '''
    kmeans_elbow_plot(df)

    Computes the intertia of inputted data for n-clusters, starting with 1-cluster and finishing at nine, and plots them on a lineplot

    args:
    df: dataframe containing the features to be fit to a cluster model

    returns: None
    '''
    inertia = []  

    #find inertia of cluster model for 1 - 9 clusters
    for i in range(1,10):
        kmeans = KMeans(n_clusters= i)
        kmeans.fit(df)
        inertia.append(kmeans.inertia_)
    sns.lineplot( range(1,10), inertia)
    plt.title('Inertias for N-Clusters')
    plt.xlabel('Inertia')
    plt.ylabel('Number of Clusters')

