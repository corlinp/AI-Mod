start:
    docker-compose run

upgrade:
	git fetch --all
	git reset origin/master --hard
	docker-compose build
	docker-compose up -d