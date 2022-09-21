


build_all: build_account build_payments build_gateway
	@echo "done building all pushing all images"

build_payments: login
	docker build -t payments ./payments
	docker tag payments csunlsrcr.azurecr.io/payments
	docker push csunlsrcr.azurecr.io/payments

build_account: login
	docker build -t account ./account
	docker tag account csunlsrcr.azurecr.io/account
	docker push csunlsrcr.azurecr.io/account

build_gateway: login
	docker build -t gateway ./gateway
	docker tag gateway csunlsrcr.azurecr.io/gateway
	docker push csunlsrcr.azurecr.io/gateway

login:
	az acr login --name csunlsrcr
