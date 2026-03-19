### Comandos Docker ###
DOCKER_COMPOSE = docker compose
ENV_LOCAL = --env-file .env
ENV_NUVEM = --env-file .env.prod

docker-up-local:
		$(DOCKER_COMPOSE) --profile local $(ENV_LOCAL) up -d database

docker-up-nuvem:
		$(DOCKER_COMPOSE) $(ENV_NUVEM) up --build etl

docker-down:
		$(DOCKER_COMPOSE) --profile local down -v

docker-stop:
		$(DOCKER_COMPOSE) --profile local stop

docker-test:
		docker exec -i postgres_enem_metrics psql -U postgres -c "CREATE DATABASE db_enem_metrics_test;"

### Execução das Pipelines ###
docker-run-renda:
		$(DOCKER_COMPOSE) --profile local $(ENV_LOCAL) run --rm etl python src/main_etl.py --pipeline renda

docker-run-redes:
		$(DOCKER_COMPOSE) --profile local $(ENV_LOCAL) run --rm etl python src/main_etl.py --pipeline redes_ensino

docker-run-todas:
		$(DOCKER_COMPOSE) --profile local $(ENV_LOCAL) run --rm etl python src/main_etl.py --pipeline todas


### Comandos Python ETL ###
PYTHON = env PYTHONPATH=etl/src .venv/bin/python
TRANS_REDES = etl/src/pipelines/comparativo_redes_ensino/transform.py
CAR_REDES = etl/src/pipelines/comparativo_redes_ensino/load.py

etl-trans-redes:
		$(PYTHON) $(TRANS_REDES)

etl-car-redes:
		$(PYTHON) $(CAR_REDES)