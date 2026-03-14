DOCKER_COMPOSE = docker compose
ENV_LOCAL = --env-file .env.local
ENV_NUVEM = --env-file .env

docker-up-local:
		$(DOCKER_COMPOSE) --profile local $(ENV_LOCAL) up --build

docker-up-nuvem:
		$(DOCKER_COMPOSE) $(ENV_NUVEM) up --build etl

docker-down:
		$(DOCKER_COMPOSE) --profile local down -v

docker-stop:
		$(DOCKER_COMPOSE) --profile local stop