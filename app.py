from flask import Flask, render_template, request
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Neo4j connection
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")

driver = GraphDatabase.driver(uri, auth=(user, password))

def search_movies(tx, query, skip=0, limit=10):
    result = tx.run("""
        MATCH (m:Movie)
        WHERE toLower(m.title) CONTAINS toLower($query)
        RETURN m.title as title, m.released as released, m.tagline as tagline
        ORDER BY m.released DESC
        SKIP $skip
        LIMIT $limit
    """, query=query, skip=skip, limit=limit)
    return [dict(record) for record in result]

def search_movies_count(tx, query):
    result = tx.run("""
        MATCH (m:Movie)
        WHERE toLower(m.title) CONTAINS toLower($query)
        RETURN count(m) as count
    """, query=query)
    return result.single()["count"]

def search_actors(tx, query, skip=0, limit=10):
    result = tx.run("""
        MATCH (a:Person)-[:ACTED_IN]->(:Movie)
        WHERE toLower(a.name) CONTAINS toLower($query)
        RETURN DISTINCT a.name as name, a.born as born
        ORDER BY a.name
        SKIP $skip
        LIMIT $limit
    """, query=query, skip=skip, limit=limit)
    return [dict(record) for record in result]

def search_actors_count(tx, query):
    result = tx.run("""
        MATCH (a:Person)-[:ACTED_IN]->(:Movie)
        WHERE toLower(a.name) CONTAINS toLower($query)
        RETURN count(DISTINCT a) as count
    """, query=query)
    return result.single()["count"]

def get_movies(tx, skip=0, limit=10):
    result = tx.run("""
        MATCH (m:Movie)
        RETURN m.title as title, m.released as released, m.tagline as tagline
        ORDER BY m.released DESC
        SKIP $skip
        LIMIT $limit
    """, skip=skip, limit=limit)
    return [dict(record) for record in result]

def get_movies_count(tx):
    result = tx.run("""
        MATCH (m:Movie)
        RETURN count(m) as count
    """)
    return result.single()["count"]

def get_actors(tx, skip=0, limit=10):
    result = tx.run("""
        MATCH (a:Person)-[:ACTED_IN]->(:Movie)
        RETURN DISTINCT a.name as name, a.born as born
        ORDER BY a.name
        SKIP $skip
        LIMIT $limit
    """, skip=skip, limit=limit)
    return [dict(record) for record in result]

def get_actors_count(tx):
    result = tx.run("""
        MATCH (a:Person)-[:ACTED_IN]->(:Movie)
        RETURN count(DISTINCT a) as count
    """)
    return result.single()["count"]

def get_movie_details(tx, movie_title):
    result = tx.run("""
        MATCH (m:Movie {title: $title})
        OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Person)
        OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Person)
        RETURN m.title as title, 
               m.released as released, 
               m.tagline as tagline,
               collect(DISTINCT {name: d.name, born: d.born}) as directors,
               collect(DISTINCT {name: a.name, born: a.born}) as actors
    """, title=movie_title)
    return dict(result.single())

def get_actor_movies(tx, actor_name):
    result = tx.run("""
        MATCH (a:Person {name: $name})-[:ACTED_IN]->(m:Movie)
        OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Person)
        RETURN m.title as title, 
               m.released as released, 
               m.tagline as tagline,
               collect(DISTINCT {name: d.name, born: d.born}) as directors
        ORDER BY m.released DESC
    """, name=actor_name)
    return [dict(record) for record in result]

@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    search_query = request.args.get('search', '')
    per_page = 10
    skip = (page - 1) * per_page

    with driver.session() as session:
        if search_query:
            movies = session.execute_read(search_movies, search_query, skip, per_page)
            actors = session.execute_read(search_actors, search_query, skip, per_page)
            movies_count = session.execute_read(search_movies_count, search_query)
            actors_count = session.execute_read(search_actors_count, search_query)
        else:
            movies = session.execute_read(get_movies, skip, per_page)
            actors = session.execute_read(get_actors, skip, per_page)
            movies_count = session.execute_read(get_movies_count)
            actors_count = session.execute_read(get_actors_count)

    total_movie_pages = (movies_count + per_page - 1) // per_page
    total_actor_pages = (actors_count + per_page - 1) // per_page

    return render_template('index.html', 
                         movies=movies, 
                         actors=actors,
                         current_page=page,
                         total_movie_pages=total_movie_pages,
                         total_actor_pages=total_actor_pages,
                         search_query=search_query)

@app.route('/movie/<title>')
def movie(title):
    with driver.session() as session:
        movie_details = session.execute_read(get_movie_details, title)
    return render_template('movie.html', movie=movie_details)

@app.route('/actor/<name>')
def actor(name):
    with driver.session() as session:
        movies = session.execute_read(get_actor_movies, name)
    return render_template('actor.html', actor_name=name, movies=movies)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000) 