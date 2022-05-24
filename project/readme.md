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
cd utils
python3 janus_loading.py
```

# Visualizing with gremlin vizualizer

Use ```janusgraph``` as the host. Test with query: 

```bash
g.V().limit(5)
```