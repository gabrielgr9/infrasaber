## O QUE É O PROJETO ##
O projeto InfraSaber se trata das ODS 9 e 10, pensando na inovação e na infraestrutura em meio a comunidade, pois sabemos da dificuldade dos mesmos, por isso foi pensado para empoderar e promover a participação de todas as pessoas. Onde elas podem ver onde encontram WIFI/CABEAMENTO GRATUITA para uso, verificam onde tem cursos, denunciam problemas da cidade e conseguem acompanhar o mesmo.

## ARQUITETURA ##

app - é nele que vai chegar os dados brutos trazidos dos clientes/adm, onde estão a estrutura de todos os dados, desde o dashboard até mesmo o do usuario, quantidade de letras, pk, fk
staging - aqui vai ser um pré processamento, trazendo uma cópia de tudo do app e deixando os dados padronizados, aqui onde será disponibilizado para ser tratado
trusted - aqui os dados já estão limpos e padronizados, ele que é usado para ser disponibilizado para cada área de atuação.
analytics - ele contém os dados que são utilizados para aparecer no dashboard, onde os moradores e a adm fazem o acompanhamento de cada coisa na própria página


## SEGUIR O PASSO A PASSO ABAIXO ##

-- COMO SUBIR O AMBIENTE --
utilizar o comando: docker compose up -d --build ### -d utilizado para voltar ao terminal

-- DISPARAR A DAG --
abrir no navegador e fazer login:  localhost:8080 
disparar a DAG manualmente: wifi_livre_sp_pipeline

#A DAG SÓ É DISPARADA MANUALMENTE APENAS NA PRIMEIRA VEZ, CASO SEJA FEITA ALGUMA ALTERAÇÃO NO CSV, IRÁ ATUALIZAR AUTOMATICAMENTE UMA VEZ AO DIA

## LIMITAÇÕES CONHECIDAS ##
CSV: foi utilizado um CSV dos pontos_internet de CARAPICUÍBA ficticíos, porque a mesma não possui dados API Pública de WIFI;

Coordenadas: pelo fato de ser um CSV fictício, as coordenadas não tem geocodificação real;

Campo Descrição: o campo descrição não foi preenchido no dado sintético por decisão própria, tendo em vista que estamos falando de internet disponibilizada pelo GOVERNO de forma GRATUITA



## TECNOLOGIAS UTILIZADAS ##

Python - o projeto foi utilizado nessa linguagem
SQLAlchemy - uma biblioteca que conecta códigos de programação ao banco de dados relacional, usado para conectar ao PostgreSQL
PostgreSQL - banco de dados onde fica guardado todos os dados do projeto
FastAPI - aqui onde inserimos (ou pegamos de fora) os dados da api para preencher os dados do banco
Docker - montada a estrutura da ordem que cada aplicação deve subir, padronizada as imagens com suas versões
Spark - utilizado para processar grandes volumes de dados de maneira rápida, no caso o CSV
Airflow - aqui onde foi feito a ETL, extração -> transformação -> carregamento
HTML - utilizado para montar as páginas de forma interativa
CSS - aqui onde está a beleza, desde a tela de login até os cards
JS - aqui onde é feito a integração do backend com o frontend
