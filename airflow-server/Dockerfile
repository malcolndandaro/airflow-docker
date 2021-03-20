# Dockerfile

# Setting up ubuntu
FROM ubuntu:20.04
RUN apt-get -y update 
RUN apt-get install -y build-essential python3.8 python3-pip python3-dev

# Timezone info
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV DEBIAN_FRONTEND=nointeractive

# Airflow requirements
RUN apt-get install -y --no-install-recommends \
         freetds-bin \
         krb5-user \
         ldap-utils \
         libffi7 \
         libsasl2-2 \
         libsasl2-modules \
         libssl1.1 \
         locales  \
         lsb-release \
         sasl2-bin \
         sqlite3 \
         unixodbc

# AIRFLOW CONFIGS
ENV AIRFLOW_HOME=/app/airflow
ENV PATH=$PATH:~/.local/bin

#20/03/2021 -BUG No SQLAlchemy > 1.4
RUN pip3 install SQLAlchemy==1.3.23

# Airflow pip install
RUN pip3 install apache-airflow

# psycopg2
RUN pip3 install psycopg2-binary

# ENTRYPOINT
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 8080

