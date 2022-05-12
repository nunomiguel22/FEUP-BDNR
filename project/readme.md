# Docker

```bash
docker-compose up -d
```

# Setting up JanusGraph

In the janusgraph CLI run:

```bash
bin/gremlin.sh
```
This will open the gremlin interface, to create a traversal object run:

```bash
g = traversal().withRemote('conf/remote-graph.properties')
```

This only needs to be done on the first time.

# Populating the database

```bash
python3 utils/janus_loading.py
```

# Visualizing with gremlin vizualizer

Use ```host.docker.internal``` as the host. Test with query: 

```bash
g.V().limit(5)
```