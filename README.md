# HowTo

Requirements:
-   Docker
-   Python
  
You may need to adapt python to python3 or pip to pip3 regarding your setup.
#### 1.  Docker Container set-up
If wanted change the credentials of Postgres and Pgadmin in the [docker-compose.yml](./super-container/docker-compose.yml)\
Navigate to the [super-container folder](./super-container/) and excecute `docker compose up`
#### 2. Install required python libraries 
Run `pip install -r .\requirements.txt`in this [folder](./)
#### 3. Set needed environment variables
Set the environment variables **POSTGRES_PASSWORD** and **POSTGRES_USER**\
These can be directly adopted from the [docker-compose.yml](./super-container/docker-compose.yml)
#### 4. Start the python scripts
Each script has to be started from its folder, so that the relative paths of the config.json work.\
First start the bridge in the [mqtt-kafkaBridge folder](./mqtt-kafkaBridge/).
Then start the mqtt publisher in the [mqtt-publisher folder](./mqtt-publisher/).\
Lastly start the processing in the [processing folder](./processing/), this needs the following arguments: `python ./processing.py worker` the log level can be set manually via the flag `-l`available levels are 'crit', 'error', 'warn', 'info', 'debug'. Please select warn or below so that the print statements get displayed.