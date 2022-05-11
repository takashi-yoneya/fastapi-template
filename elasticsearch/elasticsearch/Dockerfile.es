FROM docker.elastic.co/elasticsearch/elasticsearch:7.11.0
RUN elasticsearch-plugin install analysis-kuromoji
RUN elasticsearch-plugin install analysis-icu
