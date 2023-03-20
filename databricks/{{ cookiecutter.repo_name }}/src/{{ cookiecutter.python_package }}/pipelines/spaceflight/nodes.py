"""
This is a boilerplate pipeline 'spaceflight'
generated using Kedro 0.18.4
"""

from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession

def generate_features(data):
    data = SparkSession.builder.getOrCreate().createDataFrame(data)
    feature_cols = data.columns[:-1]
    assembler = VectorAssembler(inputCols=feature_cols, outputCol='features')
    data = assembler.transform(data)

    # convert text labels into indices
    data = data.select(['features', 'species'])
    label_indexer = StringIndexer(inputCol='species', outputCol='label').fit(data)
    data = label_indexer.transform(data)

    # only select the features and label column
    data = data.select(['features', 'label'])
    return data

def generate_predictions(data):
    reg = 0.01

    # use Logistic Regression to train on the training set
    train, test = data.randomSplit([0.70, 0.30])
    lr = LogisticRegression(regParam=reg)
    model = lr.fit(train)

    # predict on the test set
    prediction = model.transform(test)

    # evaluate the accuracy of the model using the test set
    evaluator = MulticlassClassificationEvaluator(metricName='accuracy')
    accuracy = evaluator.evaluate(prediction)
    print(accuracy)
    
    return prediction, model, {"accuracy": accuracy}