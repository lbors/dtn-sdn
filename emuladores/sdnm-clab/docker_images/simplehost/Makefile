DOCKER=docker
GROUP=sdnm
PROJECT=clab-simplehost
VERSION=latest
NAME=clab-simplehost

# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

builder: ## Build SDNML simplehost image
	@echo 'Building SDNML simplehost image' \
	&& $(DOCKER) build -t $(GROUP)/$(PROJECT):$(VERSION) -f Dockerfile .

run: ## RUN SDNML simplehost container
	@echo 'Running SDNML simplehost container' \
	&& $(DOCKER) run -itd --privileged --name $(NAME) \
    --tmpfs /run --tmpfs /run/lock \
    -v /sys/fs/cgroup:/sys/fs/cgroup:ro --cap-add=NET_ADMIN $(GROUP)/$(PROJECT):$(VERSION)

start: ## Start SDNML simplehost container
	@echo 'Starting SDNML simplehost container' \
	&& $(DOCKER) start $(NAME)

stop: ## Stop SDNML simplehost container
	@echo 'Stoping SDNML simplehost container' \
	&& $(DOCKER) stop $(NAME)

del: ## Delete SDNML simplehost container
	@echo 'Deleting SDNML simplehost container' \
	&& $(DOCKER) rm $(NAME)

del-image: ## Delete SDNML simplehost image
	@echo 'Deleting SDNML simplehost image' \
	&& $(DOCKER) rmi $(GROUP)/$(PROJECT):$(VERSION)
