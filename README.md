# ID2221-Project

In this project we built a reddit bot that when triggered by a keyword, downloads a black and white image, colorize it, and responds with the colorized image. The project is inspired by the [color model](https://richzhang.github.io/colorization/) and bot built by Richard Zhang. Only the CNN from the aforementioned author is used, everything else is written from scratch. 

We read and parse the data using Kafka and Spark-Streaming, as well as store partial results in Cassandra. Spark-Straming will if triggered by a keyword, call a Python script which downloads, colorizes and uploads a response with the colorized image. 


## Dependencies & Programs Used:

* Python version: Python 3.6.3 :: Anaconda, Inc.  
    * **Notable python packages:** 
    * caffe for conda
    * [cassandra driver for python](https://docs.datastax.com/en/developer/python-driver/3.19/)
    * [praw](https://praw.readthedocs.io/en/latest/)
    * [pyimgur](https://pyimgur.readthedocs.io/en/latest/)
    * skimage 
    * numpy
    * scipy 
* [Caffe-cpu](https://caffe.berkeleyvision.org/installation.html) (or Caffe-GPU if you have a GPU)
* Kafka: 2.11 with Scala 2.3.0
* Zookeeper: 3.4.14 
* Spark: 2.4.3 with Scala 2.11.12
* Cassandra: 3.11.2

## Color model
* See instructions in _/src/colorize\_bot/model/downloading\_the\_model.md_

## Running the program
* Update callPython function in src/reddit\_reader/RedditReader.scala with
  correct script path
* Update the [praw.ini]() file in src/reddit-reader with your credentials.
* Update the imgur_credentials.py file in src/python_scripts
* Update image_paths.py file in src/python_scripts with your full image path locations
* Start Zookeeper:
```
$KAFKA_HOME/bin/zookeeper-server-start.sh 
$KAFKA_HOME/config/zookeeper.properties
```
* Start Kafka: 
```
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
```
* Optional: Set kafka-log-retention to 10 minutes in server.properties, since we're not very interested in storing the logs for a long time. 
* Start Cassandra: 
```
$CASSANDRA_HOME/bin/cassandra -f
```
   * Create a keyspace called bot_post_keyspace
   * Create a table within keyspace: `create table Posts (postID text, imgURL text, primary key (postID));` 
* Start Kafka-Connect: See instructions in _/kafka-connect-reddit_  
If you're running kafka as a binary, change:  
```connect-standalone config/connect-standalone.properties config/kafka-connect-reddit-source.properties ```  
to  
```$KAFKA_HOME/bin/connect-standalone.sh config/connect-standalone.properties config/kafka-connect-reddit-source.properties```
* Run `sbt run` in _/src/reddit\_reader/_ 
