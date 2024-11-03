
gen_protos:
	python3 -m grpc_tools.protoc --python_out=. --grpc_python_out=. --pyi_out=. --proto_path=. ./protos/*.proto

migrate:
	alembic upgrade heads

make_migrations:
	alembic revision --autogenerate -m $(name)