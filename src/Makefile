


build_all: build_enterprise build_catalogue build_gateway
	@echo "done building all pushing all images"

build_enterprise: login
	docker build -t enterprise ./enterprise
	docker tag enterprise csunlsrcr.azurecr.io/enterprise
	docker push csunlsrcr.azurecr.io/enterprise

build_catalogue: login
	docker build -t catalogue ./catalogue
	docker tag catalogue csunlsrcr.azurecr.io/catalogue
	docker push csunlsrcr.azurecr.io/catalogue

build_gateway: login
	docker build -t gateway ./gateway
	docker tag gateway csunlsrcr.azurecr.io/gateway
	docker push csunlsrcr.azurecr.io/gateway

login:
	az acr login --name csunlsrcr
