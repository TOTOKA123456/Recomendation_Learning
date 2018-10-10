# coding=utf-8
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

from math import sqrt

def sim_distance(prefs, person1, person2):
    si = {}

    for item in prefs[person1]:         #如果两者没有相同之处，返回 0
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0:
        return 0

    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                         for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sqrt(sum_of_squares))

print('欧几里得距离：{}'.format(sim_distance(critics, 'Toby', 'Lisa Rose')))

def sim_pearson(prefs, p1, p2):
    si = {}

    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    n = len(si)
    if n == 0:
        return 1

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    sum1sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2sq = sum([pow(prefs[p2][it], 2) for it in si])
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])

    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1sq - pow(sum1, 2)/n)*(sum2sq - pow(sum2, 2)/n))
    if den == 0:
        return 0
    r = num/den
    return r

print('皮尔逊距离：{}'.format(sim_pearson(critics, 'Toby', 'Lisa Rose')))

def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other), other) for other in prefs if other != person]
  scores.sort()
  scores.reverse()
  return scores[0:n]

print(topMatches(critics, 'Toby', n=3))         #此推荐仅仅找到品味相近的人,以及相似度的值

#基于人的相似度，来进行推荐
print('='*30,'User-Based','='*30)

def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}    #{电影名：打分*相似度的总和}
    simSums = {}   #{电影名：相似度的和}
    for other in prefs:         #遍历人
        # don't compare me to myself
        if other == person: continue
        sim = similarity(prefs, person, other)
        # ignore scores of zero or lower
        if sim <= 0: continue

        for item in prefs[other]:       #遍历商品
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings
print(getRecommendations(critics, 'Toby', similarity=sim_distance))


def transformPrefs(prefs):      #把critics数据进行转化以下，item-based
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    return result
rev_critics = transformPrefs(critics)

print(topMatches(rev_critics, 'Superman Returns'))

print(getRecommendations(rev_critics, 'Just My Luck'))

#基于物品的相似度，来进行推荐
print('='*30,'Item-Based','='*30)

def calculateSimilarItems(prefs, n=10):
    result = {}
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        c+=1                     #针对大数据更新状态变量
        if c%100 == 0:
            print("%d/%d"%(c, len(itemPrefs)))
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_pearson)
        result[item] = scores
    return result
itemsim = calculateSimilarItems(critics)   #离线计算出物品相似度表

def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]   #当前用户的看电影打分情况
    scores = {}
    totalSim = {}
    for (item, rating) in userRatings.items():
        for (similarity, item2) in itemMatch[item]:     #电影相似度表
            if item2 in userRatings:
                continue
            scores.setdefault(item2, 0)
            scores[item2]+=similarity*rating
            totalSim.setdefault(item2, 0)
            totalSim[item2]+=similarity
    ranking = [(score/totalSim[item], item) for item, score in scores.items()]
    ranking.sort()
    ranking.reverse()
    return ranking

print(getRecommendedItems(critics, itemsim, 'Toby'))

#原理不记得了，翻看《集体智慧编程》p15和 p24两张表格

#电影推荐
print('='*30,'MovieLens电影推荐','='*30)
def loadMovieLens(path='E:/MovieLens/ml-latest-small/ml-latest-small'):
    movies = {}
    for line in open(path+'/movies.csv', encoding='utf8'):
        (movieId, title) = line.split(',')[0:2]
        movies[movieId] = title
    prefs = {}
    for line in open(path+'/ratings.csv', encoding='utf8'):
        (userId,movieId,rating,timestamp) = line.strip().split(',')
        prefs.setdefault(userId, {})
        prefs[userId][movies[movieId]] = float(rating)      #这里的类型转换存在一点问题
    return prefs

prefs = loadMovieLens()
print(prefs['87'])
itemsim = calculateSimilarItems(prefs, n=50)
print(getRecommendedItems(prefs, itemsim, '87')[0:30])
