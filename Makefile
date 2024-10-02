# Variables
IMAGE_NAME = ragyva
CONTAINER_NAME = ragyva
PORT=8825
CONFIG=config-prod.ini
DB_FOLDER=$(PWD)/.db

# Default target
all: build run

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run: build
	docker run --name $(CONTAINER_NAME) -d \
		-p $(PORT):8824 \
		-v $(DB_FOLDER):/app/.db \
		--add-host=host.docker.internal:host-gateway \
		-e OLLAMA_HOST=host.docker.internal \
		$(IMAGE_NAME) \
		python ./server.py --config ${CONFIG}

# Stop the Docker container
stop:
	docker stop $(CONTAINER_NAME)
	docker rm -f $(CONTAINER_NAME)

logs:
	docker logs -f $(CONTAINER_NAME)

# Remove the Docker container
clean: stop
	docker rm $(CONTAINER_NAME)
