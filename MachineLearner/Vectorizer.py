#!/Users/inosphe/anaconda/bin/python
# -*- coding:utf-8 -*-
from konlpy.tag import Mecab
import numpy as np

mecab = Mecab()

def tasks_to_vectors(tasks, word2vec):
    return [task_to_vector(task, word2vec) for task in tasks]

def tasks_to_cluster_labels(tasks, word2vec, pipe):
    vectors = tasks_to_vectors(tasks, word2vec)
    return [pipe.predict(vector) for vector in vectors]

def task_to_vector(task, word2vec):
    # 형태소 분석
    global mecab
    words = [key for key, pos in mecab.pos(task)]
    # aggregation wordvectors
    vector = np.mean(np.array([word2vec[word] for word in words if word in word2vec]), axis=0)

    return vector

def task_to_cluster_label(task, word2vec, pipe):
    vector = task_to_vector(task, word2vec)
    return pipe.predict(vector)
