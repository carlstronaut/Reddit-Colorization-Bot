package sparkstreaming

import java.util.HashMap
import org.apache.kafka.clients.consumer.ConsumerConfig
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.streaming.kafka._
import kafka.serializer.{DefaultDecoder, StringDecoder}
import org.apache.spark.SparkConf
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.storage.StorageLevel
import java.util.{Date, Properties}
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord, ProducerConfig}
import scala.util.Random

import org.apache.spark.sql.cassandra._
import com.datastax.spark.connector._
import com.datastax.driver.core.{Session, Cluster, Host, Metadata}
import com.datastax.spark.connector.streaming._
import scala.util.parsing.json.JSON
import org.apache.log4j.{Level, Logger}
import scala.sys.process._

object RedditReader {
  // Call script for colorization 
  def triggerPython(id: String, link_id: String): Unit = {
    // Change to your script path
    val scriptPath = "python /home/carl/School/Master/5/DIC/ID2221-Project/src/python_scripts/colorize_bot/color_bot.py"
    val output = Process(s"$scriptPath -comment_id $id -post_id $link_id")!
  }

  def main(args: Array[String]) {
    // Configure a spark config, running locally the computer wiht 2 cores
    val conf = new SparkConf().setAppName("redditReader").setMaster("local[2]")
    // Define a streaming context with the config, and batching interval
    val ssc = new StreamingContext(conf, Seconds(5))
    // Minimize output from Spark
    val rootLogger = Logger.getRootLogger()
    rootLogger.setLevel(Level.ERROR)
    // Kafka connection parameters, used when creating the stream
    val kafkaConf = Map(
                        "metadata.broker.list" -> "localhost:9092",
                        "zookeeper.connect" -> "localhost:2181",
                        "group.id" -> "reddit_reader_group", // Give a name to the stream group
                        "zookeeper.connection.timeout.ms" -> "1000"
                        )

    // The topic specified in the producer (we skip posts) 
    val topics = Set("reddit-comments")  
    
    //                                               KEY  ,  VAL      Serlialize     Serlialize
    val comments = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](
      ssc, kafkaConf, topics)

    // Structure we will store minimized comments in 
    case class RedditComment(
      id: String,
      body: String,
      link_id: String
    )
  
    // KEY is subreddit, VAL is comment specified in kafka-connect-reddit
    val minimizedComments = comments.map(x => x._2)
      .map(comment => {
          JSON.parseFull(comment).map(rawMap => { // Parse as JSON, transform into map
            val map = rawMap.asInstanceOf[Map[String,String]]
            // Transform into RedditComment 
            RedditComment(map.get("id").get, map.get("body").get, map.get("link_id").get)
          })
      })

    // Filter comments for keyword
    val filteredComments = minimizedComments.filter(comment => comment.get.body.split(" ").contains("colorizeme"))

    // Filtered comments is a DStream with RDD[Option[RedditComment]]
    filteredComments.foreachRDD(comments => {
      comments.collect.foreach{comment => { // Collecting.foreach => func(Option[Redditcomment])
        val c = comment.get // get => RedditComment
        val id = c.id
        val body = c.body
        val link_id = c.link_id.split("_")(1) 

        // If we found a keyword trigger, call colorize script
        triggerPython(id, link_id) 
      }
      } 
    })
    
    // Optional prints during runtime
    //val partOfDStream = filteredComments.transform( rdd => {
    //  rdd.filter(rdd.take(2).toList.contains)
    //}) 
    //partOfDStream.print

    ssc.start()
    ssc.awaitTermination()
  }
}
