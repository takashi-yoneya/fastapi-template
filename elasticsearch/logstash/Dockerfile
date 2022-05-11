FROM logstash:8.1.3

USER root
RUN apt-get update && apt-get install -y gcc libmariadb-dev curl

USER logstash
RUN rm -rf /usr/share/logstash/pipeline
COPY ./pipeline pipeline
RUN curl -o mysql-connector-java-8.0.29.jar -L https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.29/mysql-connector-java-8.0.29.jar
