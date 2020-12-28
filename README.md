# airflow
Docker-compose que utilizo para rodar [Airflow](https://airflow.apache.org/) em ambientes de dev/teste/mvp.

## O Airflow não possui uma imagem oficial?

A [imagem oficial disponibilizada pelo Airflow](https://hub.docker.com/r/apache/airflow) não possui um setup simples e intuitivo, o que dificulta a utilização para testes, projetos simples pilotos de um MVP inicial. Porém, para ambientes de produção, é recomendado que se utilize a imagem oficial seguindo todas suas guidelines.

Além da imagem oficial, o repositório [puckel/docker-airflow](https://github.com/puckel/docker-airflow) era o padrão adotado pela comunidade (até o lançamento da imagem oficial em 2020). Porém, está versão 1.10.8 e não é mais mantido, o que me fez procurar outra solução.

## Requerimentos
* docker
* docker-compose

## Estrutura 

    ├── airflow-server            # Dockerfile e entrypoint para construção da imagem
        ├── docker-entrypoint.sh  
        ├── Dockerfile          
    ├── postgres                  # Base de dados do container do Postgres
    ├── dags                      # Armazenar os dags, mapeado dentro do container do airflow
    ├── docker-compose.yml        # Arquivo compose para subir os containers
    ├── README.md

## Instalação
Docker e docker-compose

    $ sudo apt-get -y install docker.io
    $ sudo apt-get -y install docker-compose
    
Git clone

    $ sudo git clone https://github.com/malcolndandaro/airflow
    
 Build & Run
 
    $ sudo docker-compose up
    
## Acessos / Links

- Airflow UI:    [localhost:8080](http://localhost:8080)
- String Postgres:    [airflow:airflow@postgres:5432/airflow](http://airflow:airflow@postgres:5432/airflow)
- *Para acessar o Postgres de fora do container do Airflow, utilizar @localhost e realizar expose na 5432 no `docker-compose.yml`*

## Usuários

Usuário para acesso ao Airflow UI: `admin/admin` Definido no arquivo > `airflow-server/docker-entrypoint.sh`

Usuário para acesso ao Postgres: `airflow/airflow` *Este é o usuario que o Airflow utiliza para se conectar com seu backend*

## DAGS

O caminho padrão mapeado no `docker-compose.yml` para os DAGS é `./dags` este diretório que está mapeado com o `/app/airflow/dags` dentro do container, que é onde o Airflow está escaneando por novos DAGS.  
Existe um delay de até 5 minutos para que um arquivo adicionado ao diretório seja importado para o Airflow UI. Este delay é padrão e pode ser alterado atraves da variável: `AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL` que possui o valor padrão de 300 (segundos)

## Variáveis

Foram definidas algumas variáveis de ambiente no `docker-compose.yml`.

- Postgres
    - `POSTGRES_USER=airflow`       # Usuario DB
    - `POSTGRES_PASSWORD=airflow`   # Password DB
    - `POSTGRES_DB=airflow`         # Nome DB

- Airflow
   - `AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow` # String de conexão
   - `AIRFLOW__CORE__EXECUTOR=LocalExecutor`                                                       # Altera o modo de execução para LocalExecutor
   - `AIRFLOW__CORE__LOAD_EXAMPLES=False`                                                          # Não carrega os DAG's de exemplo
   - `AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True`                                                      # Exibe as configurações na UI
   - `AIRFLOW__CORE__DEFAULT_TIMEZONE=America/Sao_Paulo`                                           # Define a Timezone padrão como gmt-3
   - `AIRFLOW__WEBSERVER_DEFAULT_UI_TIMEZONE=America/Sao_Paulo`                                    # Define a Timezone da UI como gmt -3


As variáveis de ambiente relacionadas ao Airflow são utilizadas para que não seja necessário alterar o arquivo `/app/airflow/airflow.cfg` dentro do container. Outras variaveis relacionadas as configurações do Airflow podem ser consultadas neste link: [Configuration Reference](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)


## Acessando o container

Caso seja necessário acesso interno ao container do Airflow, podemos utilizar o comando `docker exec` para acessar o bash:

Encontrando o nome do container

    $ docker ps
    CONTAINER ID        IMAGE                              COMMAND                  CREATED             STATUS              PORTS                    NAMES
    c427e326a6c7        airflow-docker_airflow-webserver   "/docker-entrypoint.…"   20 hours ago        Up 34 seconds       0.0.0.0:8080->8080/tcp   airflow-docker_airflow-webserver_1
    76ac43a942d3        postgres:13.1                      "docker-entrypoint.s…"   21 hours ago        Up 35 seconds       0.0.0.0:5432->5432/tcp   airflow-docker_postgres_1

Utilizando o ID ou NAME do container para acesso 

    $ docker exec -it airflow-docker_airflow-webserver_1 bash

## Sobre o arquivo docker-entrypoint.sh

O arquivo `airflow-server/docker-entrypoint.sh` tem a finalidade de start os serviços

- airflow db init
- airflow webserver
- airflow scheduler

Seguindo o conceito de utilizar containers/microserviços, idealmente teriamos cada serviço em um container diferente, porém como o comando `airflow db init` deve ser finalizado antes dos outros dois serviços startarem, seria necessário utilizar outros scripts/healthchecks para atingir este objetivo. Fica como um ponto de melhoria para proximas versões.

## Referências
* [Airflow quickstart](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
* [puckel/docker-airflow](https://github.com/puckel/docker-airflow)