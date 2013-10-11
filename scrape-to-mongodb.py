#!/usr/bin/env python

# This example uses greenlets to scrape data and throw it in a mongoDB

import time
import datetime
import gevent
import gevent.monkey; gevent.monkey.patch_all()
import pymongo

def worker(pid, collection, target):
    # scrape the data into a dict
    print 'Worker {0}: Scraping data from {1}'.format(pid, target)
    # insert the data dict as JSON into the db collection
    collection.save({ 'pid'     : pid,
                      'date'    : datetime.datetime.utcnow() })

def main():
    # 0) fire up a mongodb, I set this guy up using Docker in about 5 minutes:
    # ./docker run -d -p 27017 rgarcia/mongodb mongod --noprealloc --smallfiles --nojournal
    # 1) Setup the database and collection
    dbhost = 'localhost'
    dbport = 49154 # set this to the docker mapped port from `./docker ps`
    # mongoDB supports Gevent green threads:
    # http://api.mongodb.org/python/current/examples/gevent.html
    print 'Creating connection to mongoDB.'
    # use_greenlets=True is unnecessary if we monkey patch above
    client = pymongo.MongoClient(dbhost,dbport,use_greenlets=True)
    # choose a database by name
    db = client.test_db_name
    # choose a collection
    collection = db.test_collection
    # delete everything in the test collection just for testing
    collection.drop()

    # 2) Spawn the worker threads
    print 'Spawning workers'
    gthreads = []
    for pid in xrange(500):
        gthreads.append(gevent.spawn(worker, pid, db.test_collection, 'http://webpage.foo'))
    print 'Joining workers'
    gevent.joinall(gthreads)

    # 3) Print out results
    for item in db.test_collection.find():
        # print item['pid']
        print item

if __name__ == '__main__':
    main()

