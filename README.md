# Semantic Search using Manticore Search Engine
This project implements a proof-of-concept semantic search solution using the Manticore Search Engine, LLMs, vector databases, Docker environment, React and Flask application. 

## Goals
- Compare semantic search with keyword-based search.
- Implement a demo search page using React for Frontend.
- Managing the backend using Flask application and python to connect to Manticore database table. 

## Technologies
- Python
- Manticore Search
- OpenAI
- Flask
- React
- Docker

  ## Project's structure 
  Below is the project directory structure:

![image](https://github.com/user-attachments/assets/21846c1e-8b8f-4496-b071-baf39e487e81)

  As shown above, the project is divided into three sections: 
  - client for handling the React application for the frontend
  - Server for managing the data and the Flask application
  - The main dockerfile and docker-compose.yml file for connecting the client and server in the docker environment.
 
  ## How to use this project

  - Clone the project URL to your local computer and have Docker installed.
  - Open WindowsPowerShell and go to the project directory where you have cloned it.
  - First, check that you have docker installed by "docker -v" command.
  - In the PowerShell, Go to the react app directory which is "client/my-app/" and run this command to install all dependencies and create the node modules folder on your local system: "npm install".
  - Copy your .env file containing your own OpenAI API key into the server folder. The file content should be like this: "OPENAI_API_KEY= (your own API key)"
  - Then, in the main directory, build the project using the "docker-compose build". It will install all dependencies and build the project containers.
  - Start the containers again by using "docker-compose up -d". Now the container is running in the background and no need to start it again.

![image](https://github.com/user-attachments/assets/f7848db7-997a-4673-8161-49b8781088a9)

  - Then, to check if the API connection works, go to the serve bash container using the command “docker-compose exec server bash” and run the “python API_connection,py” command to make sure that the API connection works. If it does, you will see this message: “OpenAI API connection is working!”.

![image](https://github.com/user-attachments/assets/23861b81-2af1-4d18-aa9f-d391c40853d4)

  - Now, Let's set up the database table by connecting to MySql and creating the table. 
        o	First we have to open the mysql by using this command: “docker exec -it manticore-search-semantic mysql -u manticore -p” 
        o	Secondly after entering the password, we can access the Manticore database.
        o	Then, we must create the table called “movies” with specific parameters to be able to perform the semantic search. Since we are using the “text-embedding-3-small” OpenAI model, the dimensions should be 1536. Use this command to create the table: 
        create table movies( title text, embedding float_vector knn_type='hnsw' knn_dims='1536' hnsw_similarity='l2' );
        o	At the moment the table is create but expectedly is without any data. Next step would be to insert the data into the movies database table. 
All of the steps above are shown in the picture below:

![image](https://github.com/user-attachments/assets/b1d3693e-de35-4a19-a100-96eafcc94d0d)

  - Next would be to insert the movies data into the Manticore database tables. Currently the data file is in the format of zip because of the file size is big. 
  - First, we have to convert it to a csv file to be able to insert it into the Manticore database table. To achieve this there is a python script named “zip_to_csv.py” and another named “load_data.py” in the server folder. 
  - Open the windows powershell and go to the server bash using this command:
      docker exec -it project-semantic-search-server-1 bash
  - Then run the “zip_to_csv.py” python command using this command:
      python data_scripts/zip_to_csv.py

All the steps above are shown in the picture below:

![image](https://github.com/user-attachments/assets/03e1f547-e7bf-4254-bc86-b065fa55b8d6)

Now, there is a new file named “embeddings_2000.csv” created in the “data” folder in the server containing all of the generated embeddings. Let’s insert them into the Manticore database movies table. 
  - Inside the server bash run the below python command to insert the data into the manticore movies table:
      python data_scripts/load_data.py

![image](https://github.com/user-attachments/assets/d3743588-2f01-4ae5-a739-f5ac16c1a6d5)

Finally, the data is inserted into the Manticore database movies table. Inside the MySQL environment run the following command and you should be able to see the first 10 rows of the data including the id, title and embedding:
Select * from movies limit 10;

![image](https://github.com/user-attachments/assets/46dd879a-977c-4e9c-89d0-5bba60e481fa)

![image](https://github.com/user-attachments/assets/3c54da43-b079-4244-8082-7174b0c942c2)


## Keyword and Semantic search

The next part of the project would be to do the keyword and semantic search based on the data in the Manticore database table which we have just inserted. 
The React app is working on the localhost port 3000. 
http://localhost:3000/
You should be able to see the React application like the picture shown below:

<img width="242" alt="image" src="https://github.com/user-attachments/assets/c727efef-38ae-4891-b064-ee2e36cf7855" />

Let’s first test the keyword search:

![image](https://github.com/user-attachments/assets/72d0330f-5aee-48bb-99dc-0b6f9dc0740b)

Now the semantic search for the same search text:

![image](https://github.com/user-attachments/assets/ba1f6bdb-c0e0-4c9d-9aca-9ca3bebceb94)

## Faceted search
The final part of the project is to do a faceted search and filtering like all e-commerce websites using the  Manticore database table. 
Here is the first look at the website:

![image](https://github.com/user-attachments/assets/686e56c6-b376-4f11-8d30-826f34a9227a)

In this view, we can first search for the products listed in the database table and then filter the results to get the most efficient results possible. 
For creating the table, the lemmatization feature is enabled on the title and description which are used to do the search on these two fields. Here is the query for creating the products table:

![image](https://github.com/user-attachments/assets/fb26092d-7bed-4f8c-b9f7-f797980d9679)

Let's do an example of how this application works. We will first do the search on the word “drill”. Then, we would do filtering on the products that belong to the category “Power Tools”.  

![image](https://github.com/user-attachments/assets/0549884f-bedd-4d48-80d5-2f74cf2ed6bf)

The next filter can be to limit the price range to be between 100 to 200 euros. 

![image](https://github.com/user-attachments/assets/6c0f274f-149a-401c-b861-c9511ad89c92)

Another possible filter could be to only limit the products that are available in the database at the moment. 

![image](https://github.com/user-attachments/assets/de68cd3f-c182-419a-a175-c3c991005e2f)

Also, we can filter the results again by their manufacturer. 

![image](https://github.com/user-attachments/assets/a7e70fb9-dcde-429f-86ba-4d0a58bab69d)

This is only one example of how this application works. The important note is that the count numbers were updated accordingly in each search and filtering step. 




