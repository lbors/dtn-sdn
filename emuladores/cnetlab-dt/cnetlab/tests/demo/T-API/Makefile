DOCKER=docker
GROUP=cpqd
PROJECT=tapi-app
VERSION=latest
PORT=8080
NAME=tapi

.PHONY: help

del: ## Delete container
	@docker rm $(NAME)

del-image: ## Delete image
	@docker rmi $(GROUP)/$(PROJECT):$(VERSION)

builder: ## Build image
	@docker build -t $(GROUP)/$(PROJECT):$(VERSION) .

run: ## Run Container
	@docker run -itd --privileged --name $(NAME) -p $(PORT):$(PORT) --cap-add=SYS_MODULE $(GROUP)/$(PROJECT):$(VERSION)

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

