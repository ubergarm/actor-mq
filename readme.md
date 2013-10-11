actor-mq
========
My attempt at implementing something similar to a distributed actor model
system based on spawning multiple gevent greenlet processes all talking 0mq.

#### Prerequisite System Setup:
I decided to skip the whole vagrant/virtualbox/docker wrap my tiny project
in a whole OS and just use virtualenv and not cry over the few odd packages. 
I must resist the constant urge to purge! Just say *NO* to *CRUFT*!!!
 
    ### install basic development files
    $ sudo apt-get install python-virtualenv  # ~62.6 MB
    $ sudo apt-get install libpython-dev      # Python.h ~34.6 MB
    $ sudo apt-get install libevent-dev       # (not libev-libevent-dev) ~2 MB
    $ virtualenv ~/projects/virtualenv
    $ source ~/projects/virtualenv/bin/activate #get into virtualenv
    ### install python dependencies
    $ pip install gevent
    $ pip install pyzmq

When you are done with everything, just type `deactivate` to get out of virtualenv.

#### Running Demos:
The good stuff:

    $ ./gevent-zeromq.py

#### Todo:

1. Look into existing implementations of Process to spawn separate threads
1. Look into existing Actor subclassed from gevent.Greenlet code
1. Extend example to do something more interesting.
1. Run benchmarks on various combinations of the above code
1. Generate pretty graphs
1. PROFIT!

#### Rants:
I built manually installed zeromq from source to appease gevent-zeromq
which insisted on being separate from zmq, but then after figuring
it all out I discovered that everying was merged into pyzmq 
on September 27th, 2013... haha...
[import zmq.green as zmq](https://github.com/zeromq/pyzmq/blob/925b9201385ba28aa79448a35a8e0345b5036e97/docs/source/eventloop.rst)

Just in case you want a different zmq ver:

    ### install zeromq from source because gevent-zeromq isn't as magic as pyzmq
    $ cd ~/projects/
    $ wget http://download.zeromq.org/zeromq-3.2.4.tar.gz
    $ tar -zxvf zeromq-3.2.4.tar.gz && rm -i zeromq-3.2.4.tar.gz
    $ cd zeromq-3.2.4
    $ ./configure --prefix=/home/username/projects/virtualenv
    $ make && make install
    $ pip install gevent-zeromq --install-option --zmq=/home/username/projects/virtualenv

#### References:
* [virtualenv](https://pypi.python.org/pypi/virtualenv)
* [actor model](http://channel9.msdn.com/Shows/Going+Deep/Hewitt-Meijer-and-Szyperski-The-Actor-Model-everything-you-wanted-to-know-but-were-afraid-to-ask)
* [gevent](http://sdiehl.github.io/gevent-tutorial/) -- concurrency based lib
* [libevent](http://libevent.org/) -- event notification library
* [0mq](http://zeromq.org/)
* [G. Peretin - EURO Python 2013 - Greenlet based concurrency](https://www.youtube.com/watch?v=b9vTUZYmtiE)
* [mongodb gevent / greenlet support](http://api.mongodb.org/python/current/examples/gevent.html)
