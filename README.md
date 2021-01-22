# Hermes - LL Code Challenge

Develop: ![<hermes>](https://circleci.com/gh/kuresto/hermes/tree/develop.svg?style=svg)

Main: ![<hermes>](https://circleci.com/gh/kuresto/hermes/tree/main.svg?style=svg)

# Sobre o projeto
Acredito que o maior desafio do projeto não foi demonstrar o que eu sei, mas sim a maestria técnica de algumas coisas. Espero ter feito o suficiente. 

```
----------- coverage: platform linux, python 3.9.1-final-0 -----------
Name                     Stmts   Miss  Cover
--------------------------------------------
hermes/__init__.py           0      0   100%
hermes/app.py               34      4    88%
hermes/base.py               6      0   100%
hermes/db.py                16      0   100%
hermes/dependencies.py      13      0   100%
hermes/enums.py             13      0   100%
hermes/logs.py              11      0   100%
hermes/models.py            84      4    95%
hermes/resources.py         39      2    95%
hermes/schemas.py           29      0   100%
hermes/settings.py           4      0   100%
--------------------------------------------
TOTAL                      249     10    96%
```

## Aonde acessar?
A API está no ar na url: http://ec2-3-138-157-51.us-east-2.compute.amazonaws.com/.

Se acessarem diretamente o link, cairão na documentação auto-gerada da API


## Sobre a licença

Escolhi a licença mais aberta possível, vocês podem saber mais sobre ela aqui: https://www.gnu.org/licenses/quick-guide-gplv3.pt-br.html

## Como rodar
Em linux/mac, dispostos do comando `make`, `docker`, `docker-compose` vocês podem rodar apenas rodando o combo:

`make setup-dev`

Ele deve instalar todas as dependencias e rodar os dockers necessários.

Vocês também podem ter um servidor local com:

`make local-server`

# Decisões sobre o Banco de Dados

Dado o teste, percebi a necessidade de maleabilidade nos dados ao serem inseridos. Um e-mail tem necessidades diferentes de uma SMS etc.

Como os bancos indicados eram relacionais, optei pelo **PostgresSql**, porém prefereria ter utilizado um Não-relacional para este caso. (Uma alternativa seria utilizar o Document Store do próprio postgre).

Segue diagrama (https://dbdiagram.io/d/6002253d80d742080a368de2)

![https://dbdiagram.io/d/6002253d80d742080a368de2](https://i.imgur.com/0xuq7Qt.png)

A decisão foi que haveria uma tabela para guardar somente os parametros utilizados, independente do conteúdo deles. Uma tabela de histórico para guardar todas as alterações mais macros, e uma tabela mãe.

Os seguintes tipos de mensagem foram adicionados:

```
start - Status inicial
in_flight - Status quando ele parte para iniciar sua execução
processing - Execução foi iniciada
success - Foi enviado com sucesso
error - Erro temporário, será reprocessado
dead - Morto, não é capaz de solução.
```


# Decisões sobre a possível arquitetura

Algumas imagens do planejamento da arquitetura, pensei como ela seria no todo e não somente minha parte... Pensei que teriamos um API Gateway por cima, com um sistema de autorização por isso não me preocupei com Autenticação. Também assumi a possibilidade de que no final uma fila de mensageria FIFO seria o ideal.

### Create

![](https://i.imgur.com/8enIB6t.png)

### Get
![](https://i.imgur.com/4rJk5Gg.png)


### Delete
Ficou faltando a validação se a mensagem já havia sido enviada, se já foi enviada, não devemos ser capazes de remove-la
![](https://i.imgur.com/PiTNMpW.png)


### Queue (processamento) (não implementado)
![](https://i.imgur.com/ZV2ceGb.png)


## FastAPI e Typing

Utilizei o FastAPI exatamente pois não conheço a equipe (entrei um pouco demais no roleplay). Preferi ser mais rigoroso no código, seguindo alguns padrões mais pesados em alguns lugares para que a nivelação seja mais fácil no futuro. (Vide o uso do Typing/FastAPI)

No entanto, deveria ter separado mais alguns arquivos.

# O que não foi feito e porquê

## Autenticação
Assumi que por ser um serviço, seria parte de um todo muito maior, com uma camada de autenticação (vide Authorizer do AWS Api Gateway).

## Listeners
Não fiz listeners pois o objetivo era apenas o salvamento no banco, porém, assumi que seria enviado para um sistema de Mensageria.

## Continuous Deployment
Não fiz porque não deu tempo, mas queria ter feito.

## HTTPS
Porque a vida cobra e não deu tempo porque eu esqueci.

