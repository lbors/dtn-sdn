DOCKER=docker
GROUP=sdnm
PROJECT=clab-stratum
VERSION=latest
NAME=clab-stratum

# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

builder: ## Build SDNML Stratum image
	@echo 'Building SDNML Stratum image' \
	&& $(DOCKER) build -t $(GROUP)/$(PROJECT):$(VERSION) -f Dockerfile .

run: ## RUN SDNML Stratum container
	@echo 'Running SDNML Stratum container' \
	&& $(DOCKER) run -itd --privileged --name $(NAME) \
    --tmpfs /run --tmpfs /run/lock \
    -v /sys/fs/cgroup:/sys/fs/cgroup:ro --cap-add=NET_ADMIN $(GROUP)/$(PROJECT):$(VERSION)

start: ## Start SDNML Stratum container
	@echo 'Starting SDNML Stratum container' \
	&& $(DOCKER) start $(NAME)

stop: ## Stop SDNML Stratum container
	@echo 'Stoping SDNML Stratum container' \
	&& $(DOCKER) stop $(NAME)

del: ## Delete SDNML Stratum container
	@echo 'Deleting SDNML Stratum container' \
	&& $(DOCKER) rm $(NAME)

del-image: ## Delete SDNML Stratum image
	@echo 'Deleting SDNML Stratum image' \
	&& $(DOCKER) rmi $(GROUP)/$(PROJECT):$(VERSION)
