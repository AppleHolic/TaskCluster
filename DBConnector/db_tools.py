__author__ = 'iljichoi'
import json
import pymongo

class Pool():
    config_path = './db_config.json' # db_name, host, port,

    def __init__(self, host_type_local=True):
        self.__load_config()
        self.host_type_local = host_type_local
        print 'Connect DB...'
        try:
            self.pool = self.__mk_pool()
            print 'Creating Pool is successed! '
        except Exception:
            raise Exception("DB Connection error")

    def __load_config(self):
        with open(self.config_path, 'r') as r:
            configs = json.load(r)

        for k, v in configs.iteritems():
            setattr(self, k, v)

    def __mk_pool(self):
        if self.host_type_local:
            return pymongo.MongoClient(
                host='mongodb://%s' % self.host, port=self.port, maxPoolSize=self.MAX_POOL_SIZE
            )
        else:
            return pymongo.MongoClient(
                host='mongodb://%s' % self.host2, port=self.port, maxPoolSize=self.MAX_POOL_SIZE
            )

    def close_connection(self):
        self.pool.close()

class QueryPool():
    def __init__(self, pool):
        self.pool = pool.pool
        self.conn = self.pool.get_database(pool.db_name)

    def insert_read_log(self, log):
        log_collection = self.conn.get_collection('article_read_log')
        log_collection.insert(log)

    def get_unparsed_content(self):
        article_collection = self.conn.get_collection('articles')
        unparsed_content = [item['content'] for item in list(article_collection.find({"$where":"this.content.length>0"}))]
        return unparsed_content

    def get_tasks(self):
        task_collection = self.conn.get_collection('tasks')
        tasks = [(item['_id'], item['name'], item['description']) for item in list(task_collection.find())]
        #print tasks
        return map(list, zip(*tasks))

    def get_article_logs(self):
        log_collection = self.conn.get_collection('article_read_log')
        #select all
        logs = [(item['_id'], item['task_title']) for item in list(log_collection.find())]
        return map(list, zip(*logs))

    def attach_task_label(self, _ids, labels):
        log_collection = self.conn.get_collection('article_read_log')
        for idx, _id, label in zip(range(len(_ids)),_ids, labels):
            if idx % 10000 == 0:
                print 'Attach task label process on %d' % idx
            log_collection.update_one({'_id': _id}, {'$set': {'label': str(label)}})
