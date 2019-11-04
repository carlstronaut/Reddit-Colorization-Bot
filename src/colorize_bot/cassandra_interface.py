from cassandra.cluster import Cluster

# Default connection is localhost
cluster = Cluster()
session = cluster.connect('bot_post_keyspace')

def add_post_value(postID, imgURL): 
    session.execute(
        """
        INSERT INTO posts (postID, imgURL)
        VALUES (%s, %s)
        """,
        (postID, imgURL)
    )

def get_post_with_ID(postID):
    rows = session.execute(
                """
                SELECT * 
                FROM posts 
                WHERE postid=%s
                """,
                (postID, )
            )
    return rows

def get_all_posts():
    rows = session.execute("SELECT * FROM posts")
    return rows

def query_is_empty(query_result):
    return len(query_result.current_rows) == 0 

def print_posts(rows):
    for row in rows:
        print(row.postid, row.imgurl)

def print_all_posts():
    print_posts(get_all_posts())
