.DEFAULT_GOAL := all

gen_optopy_pb:
	PYTHONPATH=${PYTHONPATH}:.; python3 -m grpc_tools.protoc \
	-I ./optopy/ \
	--python_out=./generated/ --grpc_python_out=./generated/ \
	./optopy/*.proto

gen_hierarchical_svc_pb:
	PYTHONPATH=${PYTHONPATH}:.; python3 -m grpc_tools.protoc \
    -I ./optopy/ -I ./hierarchical_svc/ \
	--python_out=./generated/ --grpc_python_out=./generated/ \
	./hierarchical_svc/*.proto

gen_clean:
	rm -rf ./generated/*

.PHONY : all
all : gen_optopy_pb gen_hierarchical_svc_pb
