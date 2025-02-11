# RID190521_Desafio06

## Introdução

Para a elaboração do desafio, foram utilizadas as ferramentas:
 - **Docker**: plataforma de contêinerização que permite empacotar e isolar aplicações e suas dependências em ambientes virtuais, garantindo consistência e facilidade de deployment. 
 - **Apache Airflow**: ferramenta de orquestração de workflows que automatiza, monitora e gerencia tarefas complexas, permitindo a criação de pipelines de dados de forma eficiente e escalável.

Ambas as ferramentas foram integradas para automatizar as funções definidas pela análise de dados, com as funções divididas em arquivos distintos para maior organização e eficiência no processo.
   
  ### /airflow/dags/app/**extractor_loader.py**
  - Define as funções usadas para extrair e carregar dados, extraindo dados de arquivos .csv e salvando-os nos formatos .csv e .parquet.
  
  
  ### /airflow/dags/app/**transformer.py**
   - Define funções para transformar os dados conforme as necessidades observadas nos notebooks.

  
  ### /airflow/dags/app/**organizer.py**
   - Organiza as funções para a DAG principal, melhorando a clareza e manutenção do código.

  
  ### /airflow/dags/**orders_dag.py**
   - Define e configura a DAG, estabelecendo as tarefas e a ordem de execução.

  
  ### bronze_data_analysis.ipynb
   - Este arquivo analisa os dados extraídos, verificando valores nulos, erros de preenchimento e formatos incorretos de datas. Também testa algumas soluções que são aplicadas nas DAGs, nos arquivos Transformer.py e Extractor_loader.py.
 
  
  ###  silver_data_analysis.ipynb
   - Este arquivo analisa os dados limpos, criando novas colunas e explorando-os por meio de diversos métodos de agrupamento.


## Estrutura do Projeto

**Dados Brutos:** Arquivo .csv fornecido pelo desafio.
**Camada Bronze:** Lê os dados brutos do .csv e os armazena em um repositorio distinto identificando-o com a data de extração.
**Camada Prata:** Limpa e transforma os dados, preservando a data da extração.
**Camada Ouro:** Armazena os dados finais processados em formato .parquet, com agregações importantes salvas em .csv.


## Etapas de Desenvolvimento

### Etapa 1) Configuração Inicial


 - Criou-se um ambiente virtual e Instale os pacotes necessários:

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
```

 - Inicializou-se e iniciou-se o Docker:

a) Criou-se o diretorio airflow

```bash
mkdir airflow
cd airflow
```

b) Obteve-se o docker-compose.yaml

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml'
```
  - Editou-se o arquivo acrescentando o caminho para a pasta dados em:

```Yaml
 volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data
```

c) Criou-se os diretórios necessários:

```bash
mkdir -p ./dags ./logs ./plugins ./config ./data
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

d) Inicializou-se o Airflow:

```bash
docker-compose up airflow-init
```

e) Iniciou-se a execução:

```bash
docker-compose up -d
```

f) Acessou-se a interface web do Airflow:

Em um browser, acessou-se o endereço <http://localhost:8080> para supervisionar a execução das DAGs

![image](https://github.com/user-attachments/assets/eeb72edd-ae7e-495c-afbd-e423f9ce7268)


### Etapa 02) Criando o DAG no Airflow

Definiu-se o layout do projeto.

 - Criou-se o arquivo **orders_dag.py** que ficou responsavel apenas por criar e ordenar as tarefas

 - Criou-se os arquivos  **extractor_loader.py** e **transformer.py** para definir as funções executadas pelo pipeline

 - Criou-se o arquivo **organizer.py** para chamar as funções na ordem que devem ser executadas.


## Etapa 03) Processamento e Limpeza de dados

  a) Carregar Dados Brutos na Camada Bronze:
  
   - No arquivo /airflow/dags/app/**organizer.py**, definiu-se a função 
  
  ```py     
    def bronze_protocol():
  ```
  
  Que executa:
   
    * Definir nome e endereço do arquivo na camada Raw
    * Definir endereço de destino (camada Bronze)
    * Salvar os dados do arquivo Raw em um DF
    * Salvar o DF em um .csv na camada bronze, adicionando a data da execução no nome do arquivo

   - No arquivo /airflow/dags/**orders_dag.py** definiu-se a task

  ```py 
    task_1 = PythonOperator(
        task_id="bronze_protocol",
        python_callable = bronze_protocol,
        dag=dag,)
  ```


  b) Limpeza de Dados para a Camada Prata:

  - No arquivo bronze_data_analysis.ipynb, explorou-se os dados extraidos
    
  - No arquivo /airflow/dags/app/**organizer.py**, definiu-se a função 

  ```py     
    def silver_protocol():
  ```
 Que executa:
   
    * Definir nome e endereço do arquivo na camada Bronze
    * Encontrar o arquivo na camada bronze com a data correspondente a execução do código
    * Definir endereço de destino (camada Prata)
    * Salvar os dados do arquivo Bronze em um DF
    * Dropar colunas com dados nulos
    * Corrigir formato dos dados
    * Corrigir email adicionando @ aos que não possuem
    * CalculaR a idade com base na data de nascimento
    * Salvar o DF em um .csv na camada prata, adicionando a data da execução no nome do arquivo



  - No arquivo /airflow/dags/**orders_dag.py** definiu-se a task

  ```py 
    task_2 = PythonOperator(
        task_id="silver_protocol",
        python_callable = silver_protocol,
        dag=dag,)
  ```


## Etapa 04) Transformação e Armazenamento de Dados

- No arquivo silver_data_analysis.ipynb, explorou-se os dados extraidos
    
- No arquivo /airflow/dags/app/**organizer.py**, definiu-se a função 

  ```py     
    def gold_protocol():
  ```
  Que executa:

      * Definir nome e endereço do arquivo na camada Silver
      * Encontrar o arquivo na camada Silver com a data correspondente a execução do código
      * Definir endereço de destino (camada Gold)
      * Salvar os dados do arquivo Silver em um DF
      * Calcular o tempo de inscrição em anos
      * Definir os grupos de idade
      * Savar arquivos .parquets agrupados pelo grupo de idade na camada ouro e identificados pela data de execução 
      * Savar arquivos .parquets agrupados pelo status da inscrição na camada ouro e identificados pela data de execução 
      * Aggregar dados pelo grupo de idade
      * Salvar dados agregados por grupo de idade na camada ouro, identificados pela data de execução 
      * Aggregar dados pelo status da inscrição
      * Salvar dados agregados por status da inscrição camada ouro, identificados pela data de execução 
   
- No arquivo /airflow/dags/**orders_dag.py** definiu-se a task

  ```py 
    task_2 = PythonOperator(
        task_id="silver_protocol",
        python_callable = silver_protocol,
        dag=dag,)
  ```

- Define-se a ordem das tasks

```py 
  task_1 >> task_2 >> task_3
 ```
