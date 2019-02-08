# Apache Log Processing

### RUN

#### Dev:
    
    git clone https://github.com/assigdev/logs_proc
    docker-compose up -d
    docker-compose exec backend python manage.py migrate
    docker-compose exec backend python manage.py parse_logs

goto [http://0.0.0.0:8000](http://0.0.0.0:8000)

#### Stage:
    git clone https://github.com/assigdev/logs_proc
    docker-compose -f docker-compose.yaml -f docker-compose.stage.yaml up -d
    docker-compose -f docker-compose.yaml -f docker-compose.stage.yaml exec backend python manage.py migrate
    docker-compose -f docker-compose.yaml -f docker-compose.stage.yaml exec backend python manage.py parse_logs
    

goto [http://0.0.0.0](http://0.0.0.0)