# Docker

```bash
docker-compose up -d
```

# Setting up JanusGraph (Optional)

Run this step if you want to interface directly with JanusGraph using the gremlin CLI.

In the janusgraph CLI run:

```bash
bin/gremlin.sh
```
This will open the gremlin interface, to create a traversal object run:

```bash
g = traversal().withRemote('conf/remote-graph.properties')
```

# Populating the database

```bash
cd utils
python3 janus_loading.py
```

# Visualizing with gremlin vizualizer (Optional)

Use ```janusgraph``` as the host. Test with query: 

```bash
g.V().limit(5)
```

# Flask Container
On first setup Flask could fail if JanusGraph and the backends take too much time to start or even the database is empty and needs to be populated first. If so just restart the flask container when JanusGraph is ready and the DB populated.