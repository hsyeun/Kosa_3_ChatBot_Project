from gensim.models import Word2Vec

model = Word2Vec.load('nvmc.model')

print(model.wv.most_similar('영화관',topn=3))