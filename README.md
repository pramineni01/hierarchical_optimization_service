# Hierarchical Optimization Service

### How to run
```
pip install -r requirements.txt
cd hierarchical_optimization_service/
```

### Generate code from protos
```
cd main/proto
make gen_clean # for clearing pre-existing generated code, if any
make
```
### Start server
```
cd hierarchical_optimization_service/main
python assetsim_interface_server/server.py
```

### Run client
```
cd hierarchical_optimization_service/main
python assetsim_interface_client/test_client.py
```
