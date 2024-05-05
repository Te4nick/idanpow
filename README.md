# IDANPOW
idanpow API - Integration and Deployment Architecture course project

## Run in Docker Compose

- Clone repository
- Copy docker/django/.env.example to docker/django/.env 
  and change values if needed ($HOST and $PORT entries are tied to docker-compose.yml,
  so you need to also modify compose file, $DEBUG stands for django DEBUG mode, 
  supported values are 0 and 1). 
  ```bash
  $ cp docker/django/.env.example docker/django/.env
  ```
- Run Docker Compose
  ```bash
  $ docker compose up
  ```