# 推荐系统
## 协同过滤
* recommendation.py 协同过滤算法基础版，《集体智慧编程》书籍第二章协同过滤
* 相似度计算：欧几里得距离、皮尔逊距离
* topMatches(prefs,person,n=5,similarity=sim_pearson)，做基于人/商品的相似度排序，取top N
* getRecommendations(prefs, person, similarity=sim_pearson)，做基于人的推荐，CF原理可见 P15 页表格
* transformPrefs(prefs)，把critics数据进行转化一下
* calculateSimilarItems(prefs, n=10)，离线计算出物品相似度表
* getRecommendedItems(prefs, itemMatch, user)，实现基于商品的推荐，原理可见 P24 页表格
* loadMovieLens(path='E:/MovieLens/ml-latest-small/ml-latest-small')，导入movielens数据，做电影推荐
## 基于Neo4j网络结构的推荐
* 主页推荐、图书相关推荐
* 将关系型数据库——>图数据库，构建网络
* 定义规则，进行图查询，py2neo连接
