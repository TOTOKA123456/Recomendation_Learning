# coding=utf-8
from surprise import Dataset
from surprise import Reader
from surprise import accuracy
from surprise import NMF
from surprise import SlopeOne
from surprise.model_selection import train_test_split
from surprise import dump

filePath = r'E:\library\Final_lib\collaboration\coll2.csv'
reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 5))
data = Dataset.load_from_file(filePath, reader=reader)

trainset, testset = train_test_split(data, test_size=0.2)
# algo = BaselineOnly()
# algo.fit(trainset)
algo = SlopeOne()
algo.fit(trainset)

predictions = algo.test(testset)
accuracy.mae(predictions)
accuracy.rmse(predictions)
accuracy.fcp(predictions)

dump.dump(r'E:\library\Final_lib\collaboration\ungrouped_algo\SlopeOne.txt', predictions=predictions, algo=algo)
