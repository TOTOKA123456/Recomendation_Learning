# 协同过滤——基础知识

《集体智慧编程》书籍第二章协同过滤

1.相似度计算：欧几里得距离、皮尔逊距离

2.topMatches(prefs,person,n=5,similarity=sim_pearson)，做基于人/商品的相似度排序，取top N

3.getRecommendations(prefs, person, similarity=sim_pearson)，做基于人的推荐，CF原理可见 P15 页表格

4.transformPrefs(prefs)，把critics数据进行转化一下

5.calculateSimilarItems(prefs, n=10)，离线计算出物品相似度表

6.getRecommendedItems(prefs, itemMatch, user)，实现基于商品的推荐，原理可见 P24 页表格

7.loadMovieLens(path='E:/MovieLens/ml-latest-small/ml-latest-small')，导入movielens数据，做电影推荐
