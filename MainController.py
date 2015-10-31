#/Users/inosphe/anaconda/bin/python
# -*- coding: utf-8 -*-
from DBConnector.db_tools import Pool, QueryPool
from base_config import WORD2VEC_LINE_TEXT, WORD2VEC_MODEL, PIPE_DUMPING, CLUSTERING_METHOD, CLUSTERING_OPTION
from TextProcedure.TextParser import law_contents_to_file
from MachineLearner import Trainer
import gensim
import os
import sys

query_pool = QueryPool(Pool())
#webserver_query_pool = QueryPool(Pool(host_type_local=False))

def train_or_load_word2vec(delete=False):
    # load articles from db
    if os.path.exists(WORD2VEC_LINE_TEXT):
        if delete:
            os.remove(WORD2VEC_LINE_TEXT)
        else:
            print 'line_file_exists'
    else:
        print 'Load Article Contents.....'
        contents = query_pool.get_unparsed_content()

        # do text processing and mk word2vec line file
        print 'Proceed text filtering and mk word2vec_line_text'
        law_contents_to_file(contents, WORD2VEC_LINE_TEXT)
    if os.path.exists(WORD2VEC_MODEL):
        if delete:
            os.remove(WORD2VEC_MODEL)
        else:
            return gensim.models.Word2Vec.load_word2vec_format(WORD2VEC_MODEL, binary=True)
    # training!
    return Trainer.train_and_save_vector(WORD2VEC_LINE_TEXT, WORD2VEC_MODEL)


def task_clustering(method, option, word2vec=None):
    # load db from remote
    _ids, tasks = query_pool.get_article_logs()

    # word2vec load
    if word2vec is None:
        word2vec = gensim.models.Word2Vec.load_word2vec_format(WORD2VEC_MODEL, binary=True)

    # create and dump pipe
    # percentage 는 전체 태스크 수를 클러스터링 했을 때 한 클러스터의 차지하는 비중
    print 'Start Clustering'
    pipe, labels = Trainer.decompose_and_cluster(tasks, word2vec, PIPE_DUMPING, method=method, option=option)

    # update task db
    query_pool.attach_task_label(_ids=_ids, labels=labels)

def main():
    word2vec = train_or_load_word2vec(delete=False)
    task_clustering(method=CLUSTERING_METHOD, option=CLUSTERING_OPTION, word2vec=word2vec)

if __name__=='__main__':
    main()
