# Semantic Search using Manticore Search Engine
This project implements a proof-of-concept semantic search solution using the Manticore Search Engine, LLMs, vector databases, Docker environment, React and Flask application. 

## Goals
- Compare semantic search with keyword-based search.
- Implement a demo search page using React for Frontend.
- Managing the backend using Flask application and python to connect to Manticore database table. 

## Technologies
- Python
- Manticore Search
- SentenceTransformers
- Flask
- React
- Docker

  ## Project's structure 
  Below is the project directory structure:

<img width="341" alt="image" src="https://github.com/user-attachments/assets/85ae8e9b-79b7-4537-82f9-aa82d42db4e3">

  As shown above, the project is divided into three sections: 
  - client for handling the React application for the frontend
  - Server for managing the data and the Flask application
  - The main dockerfile and docker-compose.yml file for connecting the client and server in the docker environment.
 
  ## How to use this project
  - Clone the project URL to your local computer and have Docker installed.
  - Open WindowsPowerShell and go to the project directory where you have cloned it.
  - First, check that you have docker installed by "docker -v" command.
  - In the PowerShell, Go to the react app directory which is "client/my-app/" and run this command to install all dependencies and create the node modules folder on your local system: "npm install"
  - Then, in the main directory, build the project using the "docker-compose build". It will install all dependencies and build the project containers.
  - Start the containers again by using "docker-compose up -d". Now the container is running in the background and no need to start it again.
  - Let's set up the database table by connecting to MySql and creating the table, shown in the picture below:
<img width="668" alt="image" src="https://github.com/user-attachments/assets/a4489f56-6623-4144-b6f4-656765e7b39f">

  - Next would be to insert the movies data into the Manticore database table. In the PowerShell, go to the server bash and run the "load_data.py" script, shown as below:
<img width="577" alt="image" src="https://github.com/user-attachments/assets/d0aa8392-3609-4c45-9b30-a760d2fedf3b">

- After that, we can go to the database table and see the data in the movies database table, below is just a small part of the data. 
<img width="666" alt="image" src="https://github.com/user-attachments/assets/ec152e48-6e0f-4100-a084-1d51f9c9b9ae">

We have the client and server both running in the docker and are connected. As a test, I created a component in the React app, and below is the test result:

Server working:

<img width="300" alt="image" src="https://github.com/user-attachments/assets/045aee5a-5dc9-4b24-b02b-88b81b9db512">

Client working:

<img width="595" alt="image" src="https://github.com/user-attachments/assets/1c7716b9-803c-4ce9-8e12-3f7b838fb3dc">


## Full-text search
- The server is running on "http://localhost:80/search?query=(put-the-search-word)" and the Client is running on "http://localhost:3000/".
- Full-text search is working on the backend currently as shown below with a few tests:

<img width="314" alt="image" src="https://github.com/user-attachments/assets/81fffba8-e9bc-439e-808c-46f08eb36b47">
<img width="292" alt="image" src="https://github.com/user-attachments/assets/497d9461-a0ef-4801-9d02-885de8698980">


- Full-text search is also working in the react app and functioning completely.
<img width="232" alt="image" src="https://github.com/user-attachments/assets/78a3831a-06b4-467c-80d4-f79ae0186ae1">

## Semantic search
The next stage of the project is to implement semantic search and to be able to compare both searches together. Below is the search buttons feature which only now the keyword search works.

<img width="231" alt="image" src="https://github.com/user-attachments/assets/14c0c501-45c4-4c8d-975c-56dc5b082f63">
<img width="238" alt="image" src="https://github.com/user-attachments/assets/594c4fb4-d124-4899-8654-8c9ff8152392">



The next step would be implementing the semantic search on both the Flask and React applications. 
