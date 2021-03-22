IMG=strat_api
APP=strategies_api

.PHONY: run 
run: 
	python3 src/main.py

.PHONY: gen-protos 
gen-protos:
	@python -m grpc_tools.protoc -I.\
	       	--python_out=./src/generated --grpc_python_out=./src/generated \
		./src/proto/echo.proto
	@echo "Generated protobufs"
	@mv src/generated/src/proto/*.py src/generated

.PHONY: docker-build 
docker-build: 
	docker build -t $(IMG):latest . 

.PHONY: docker-run 
docker-run: 
	docker run --name $(APP) $(IMG)

.PHONY: docker-down
docker-down:
	docker stop $(APP)
	docker rm $(APP)
