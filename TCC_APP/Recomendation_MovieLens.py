import pandas as pd
import pymysql
import numpy as np
import csv
from sqlalchemy import create_engine

db = pymysql.connect(host='watchlist.mysql.database.azure.com',user='tccapp',password='yE2KGUn7!Nqchvd',db='app_db')
engine = create_engine("mysql+pymysql://tccapp:yE2KGUn7!Nqchvd@watchlist.mysql.database.azure.com/app_db")
cursor = db.cursor()

query_recommend = ('Select index as title from recommend_temp')
query_movies = ('Select * from movies')
#query_ratings = ('Select * from items')


## Lendo o conjunto de dados do MovieLens.
#df_f = pd.read_sql(query_movies, db).drop(['poster'],axis=1)
#df_av = pd.read_sql(query_ratings, db)
df_f = pd.read_csv("movies.csv")
df_av = pd.read_csv("ratings.csv")

## Juntando os dois arquivos .csv com a função merge do pandas e retirando as colunas que não vamos utilizar.
df_av = pd.merge(df_f,df_av).drop(['genres'],axis=1)

## Criação da Matriz, onde o ID do Usuário será nossas linhas, o titúlo do video a nossas colunas e seram populados pelas avaliação dos usuários.
df_av_u = df_av.pivot_table(index=['owner_id'],columns=['title'],values='rating')

## Um problema recorrente para algoritmos de filtro colaborativo, é a esparsidade dos dados coletados, para otimizar o nosso código, vamos ignorar os filmes que tem menos de 10 avaliaçãos de usuários.
df_av_u = df_av_u.dropna(thresh=10,axis=1).fillna(0)

## Aplicação do método de Coeficiente de Correlação de Pearson, para obter o valor de similadirade entre os filmes através das avaliações do usuários.
pearson = df_av_u.corr(method='pearson')


## Função que calcula o valor que será considerado para recomendar um filme ou não.
## Ele pega o valor de Pearson que definimos e multiplica esse valor pela avaliação do usuário.
def recomendacao (f, au):
    ps = pearson[f]*(au)
    return ps

## Avaliação de usuários teste.
user = [('Avatar (2009)',4),
        ('Lion King, The (1994)',5),
        ('Fast and the Furious, The (2001)',3.5),
        ('Toy Story (1995)',5),
        ('Jurassic Park (1993)',4.5),
        ('Twilight (2008)',4),
        ('Pride & Prejudice (2005)',3.5),
        ('Notebook, The (2004)',3),
        ('17 Again (2009)',5),
        ('Twilight Saga: Eclipse, The (2010)',2),
        ('Aladdin (1992)',5),
        ('Beauty and the Beast (1991)',4),
        ('Mrs. Doubtfire (1993)',3),
        ('Toy Story 2 (1999)',5),
        ('Hangover, The (2009)',2),
        ('Harry Potter and the Goblet of Fire (2005)',2)
        ]


## Criação de dataframe para definir filmes para recomendar ao nosso usuário
df_fs = pd.DataFrame()

## Loop que inseri os valores calculados pela função de recomendação em um dataframe
for f,a in user:
    df_fs = df_fs.append(recomendacao(f,a))

df_fs.to_csv("teste3.csv")

## Inserindo linha com a soma total dos valores da coluna para definir o valor de recomendação do filme.
df_fs.loc['Total']= df_fs.sum(numeric_only=True, axis=0)


## Retirando as colunas que contém os filmes já avaliados pelo usuário.
df_fs2 = df_fs
df_fs2.drop(['Avatar (2009)',
            'Lion King, The (1994)',
            'Fast and the Furious, The (2001)',
            'Wedding Crashers (2005)',
            'Toy Story (1995)',
            'Jurassic Park (1993)',
            'Twilight (2008)',
            'Pride & Prejudice (2005)',
            'Notebook, The (2004)',
            '17 Again (2009)',
            'Twilight Saga: Eclipse, The (2010)',
            'Aladdin (1992)',
            'Beauty and the Beast (1991)',
            'Mrs. Doubtfire (1993)',
            'Toy Story 2 (1999)',
            'Hangover, The (2009)',
            'Harry Potter and the Goblet of Fire (2005)'
            ],axis=1, inplace=True)

## Transpondo o arquivo .csv para ordenar pela coluna "Total".

df_fs3 = df_fs2.transpose()
df_fs4 = df_fs3.sort_values(by="Total",ascending=False)
df_fs4.to_csv('recomendacoes2.csv', encoding='utf-8')
df_fs5 = df_fs4.drop(df_fs4.columns[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]],axis = 1)
df_fs6 = df_fs5.head(40)
df_fs6.to_csv('recomendacoes.csv', encoding='utf-8')
header = ["title"]
df_fs8 = pd.read_csv ("recomendacoes.csv", header=None, skiprows=1, names=header)
df_fs9 = pd.merge(df_fs8, df_f, on= 'title').drop(['genres'],axis=1)
df_fs10 = df_fs9.assign(userID=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
df_fs11 = df_fs10.assign(id=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39])
df_fs12 = df_fs11.sort_index(axis=1)


# ---------------------------------------------------------------- UPDATE DATABASE COM RECOMENDACAO -------------------------------------------------------------------------------- # 

cursor.execute('DROP TABLE IF EXISTS recommend_temp')
cursor.execute('DROP TABLE IF EXISTS recommend_temp2')
#cursor.execute('CREATE TABLE recommend_temp(id int PRIMARY KEY, title varchar(255), movieId int, userId int)')
cursor.execute('CREATE TABLE recommend_temp2(id int PRIMARY KEY, title varchar(255), movieId int, description text, poster longtext, userId int)')

#csv_data = csv.reader(open('recomendacoes.csv'))
#next(csv_data)
#for row in csv_data:
#    cursor.execute('INSERT INTO recommend_temp(id, title, movieId, userId) VALUES (%s,%s,%s,%s)',row)

df_fs12.to_sql(name= 'recommend_temp', con=engine, index=False)

cursor.execute('INSERT INTO recommend_temp2 (SELECT recommend_temp.id, recommend_temp.title, recommend_temp.movieId, movies.description, movies.poster, recommend_temp.userId FROM recommend_temp LEFT JOIN movies ON app_db.recommend_temp.movieId = movies.movieId)')
cursor.execute('UPDATE recommend INNER JOIN recommend_temp2 ON recommend.id = recommend_temp2.id SET recommend.title = recommend_temp2.title, recommend.movieId = recommend_temp2.movieId, recommend.description = recommend_temp2.description, recommend.poster = recommend_temp2.poster  where recommend_temp2.id >= 0')

cursor.execute('DROP TABLE IF EXISTS recommend_temp')
cursor.execute('DROP TABLE IF EXISTS recommend_temp2')
db.commit()
cursor.close()
