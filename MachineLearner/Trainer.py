__author__ = 'iljichoi'
import gensim
import numpy as np
import os
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from Vectorizer import tasks_to_vectors

def train_and_save_vector(input_file, output_file):
    line_obj = gensim.models.word2vec.LineSentence(input_file)
    print 'Start to train word2vec model'
    model = gensim.models.Word2Vec(line_obj, size=200, window=5, min_count=2, workers=3)

    if os.path.exists(output_file):
        os.remove(output_file)

    print 'End of training, Start to save....'
    model.save_word2vec_format(output_file, binary=True)

    return model

def decompose_and_cluster(tasks, word2vec, output_file, method='DBSCAN', option=0.5):
    """
        You should pass parameter 'method', 'option' as follows
        method = 'DBSCAN' or 'KMeans'
        option = eps or n_clusters
    """
    print 'Get task vector'
    whole_vector = tasks_to_vectors(tasks, word2vec)
    print 'Down dimension...'
    pca = PCA(5)
    d_vector = pca.fit_transform(whole_vector)
#    print 'PCA Log Likelihood Score : ' + str(pca.score())

    if method=='KMeans':
        print 'Training K-means...'
        cluster = KMeans(n_clusters=option, n_jobs=3)
    else:
        print 'Training DBSCAN ... '
        cluster = DBSCAN(eps=option)

    cluster.fit(d_vector)
    labels = cluster.predict(d_vector)

    pipe = Pipeline(steps=[
        ('w2v_200_to_5_PCA', pca), ('clustering', cluster)
    ])
    if os.path.exists(output_file):
        os.remove(output_file)
    joblib.dump(pipe, output_file, compress=3)
    print 'Complete dumping'

    return pipe, labels
