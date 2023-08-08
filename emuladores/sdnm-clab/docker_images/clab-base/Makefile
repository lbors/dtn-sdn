DOCKER=docker
GROUP=sdnm
PROJECT=clab-debian
VERSION=11
NAME=clab-debian

# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

builder: ## Build SDNML nmstate image
	@echo 'Building SDNML nmstate image' \
	&& $(DOCKER) build -t $(GROUP)/$(PROJECT):$(VERSION) -f Dockerfile .

run: ## RUN SDNML nmstate container
	@echo 'Running SDNML nmstate container' \
	&& $(DOCKER) run -itd --privileged --name $(NAME) \
    --tmpfs /run --tmpfs /run/lock \
    -v /sys/fs/cgroup:/sys/fs/cgroup:ro --cap-add=NET_ADMIN $(GROUP)/$(PROJECT):$(VERSION)

start: ## Start SDNML nmstate container
	@echo 'Starting SDNML nmstate container' \
	&& $(DOCKER) start $(NAME)

stop: ## Stop SDNML nmstate container
	@echo 'Stoping SDNML nmstate container' \
	&& $(DOCKER) stop $(NAME)

del: ## Delete SDNML nmstate container
	@echo 'Deleting SDNML nmstate container' \
	&& $(DOCKER) rm $(NAME)

del-image: ## Delete SDNML nmstate image
	@echo 'Deleting SDNML nmstate image' \
	&& $(DOCKER) rmi $(GROUP)/$(PROJECT):$(VERSION)
