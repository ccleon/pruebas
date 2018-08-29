# Orden
## Filebeat
* cd filebeat
* ./filebeat -c filebeat.yml &

## Elasticsearch
* ./elasticsearch/bin/elasticsearch
* Nota: si queremos borrar la base de datos tenemos que ejecutar curl -X DELETE "localhost:9200/*"

## Logstash
* cd logstash
* ./bin/logstash -f logstash.conf &


## Mininet
* cd Repositories/prueba
* sudo python toponew.py (no hace falta ODL porque está el controlador por defecto)
