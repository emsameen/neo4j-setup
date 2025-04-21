# Neo4j Movies Database Web Application

A web application that showcases the Neo4j Movies database, providing an interactive interface to explore movies, actors, and directors.

## Features

- **Movie Exploration**
  - Browse a list of movies with their titles, release years, and taglines
  - View detailed information about each movie
  - See all actors who appeared in a movie
  - View director information when available

- **Actor Exploration**
  - Browse a list of actors with their names and birth years
  - View all movies an actor has appeared in
  - See director information for each movie
  - Navigate between actors and their movies

- **Interactive Navigation**
  - Easy navigation between movies and actors
  - Clickable links to explore relationships
  - Responsive design for all screen sizes
  - Clean and intuitive user interface

## Technical Stack

- **Backend**
  - Python 3.11
  - Flask web framework
  - Neo4j database driver

- **Frontend**
  - Bootstrap 5.3
  - Jinja2 templating
  - Responsive design

- **Infrastructure**
  - Docker
  - Docker Compose
  - Neo4j database

## Setup Instructions

1. **Prerequisites**
   - Docker
   - Docker Compose
   - Git (optional)

2. **Clone the Repository** (if using Git)
   ```bash
   git clone <repository-url>
   cd neo4j-setup
   ```

3. **Environment Setup**
   - The application uses environment variables for Neo4j connection
   - Default values are set in the code:
     - NEO4J_URI: bolt://localhost:7687
     - NEO4J_USER: neo4j
     - NEO4J_PASSWORD: password

4. **Build and Run**
   ```bash
   docker-compose up --build
   ```

5. **Access the Application**
   - Web interface: http://localhost:3000
   - Neo4j Browser: http://localhost:7474
     - Username: neo4j
     - Password: password

6. **Initialize the Movies Database**
   - Open Neo4j Browser at http://localhost:7474
   - Log in with the credentials above
   - In the command bar at the top, type `:play movies`
   - Click on the "Movies" guide that appears
   - Follow the guide to create the sample database
   - The web application will now be able to display movie and actor data

## Usage Guide

1. **Home Page**
   - View lists of movies and actors
   - Click on any movie or actor to see details

2. **Movie Details**
   - View movie information
   - See all actors in the movie
   - Check director information
   - Navigate to actor pages

3. **Actor Details**
   - View actor information
   - See all movies the actor appeared in
   - Check director information for each movie
   - Navigate back to movie details

## Data Structure

The application uses the Neo4j Movies database which contains:
- Movies with properties: title, released, tagline
- People (actors/directors) with properties: name, born
- Relationships:
  - ACTED_IN: Person → Movie
  - DIRECTED: Person → Movie

## Troubleshooting

1. **Connection Issues**
   - Ensure Neo4j is running and accessible
   - Check environment variables
   - Verify port mappings in docker-compose.yml

2. **Data Not Loading**
   - Verify Neo4j database is properly initialized
   - Check if the Movies database is loaded
   - Ensure proper permissions

## Contributing

Feel free to submit issues and enhancement requests!
