# Copyright 2021 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example nodes to solve some common data science problems using PySpark,
such as:
* Train a machine learning model on a training dataset
* Make predictions using the model
* Evaluate the model based on its prediction
"""
import logging
from typing import Any, Dict

from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import DataFrame


def train_model(
    training_data: DataFrame, parameters: Dict[str, Any]
) -> RandomForestClassifier:
    """Node for training a random forest model to classify the data.
    The number of trees is defined in conf/project/parameters.yml
    and passed into this node via the `parameters` argument.
    For more information about random forest classifier with spark, please visit:
    https://spark.apache.org/docs/latest/ml-classification-regression.html#random-forest-classifier
    """
    classifier = RandomForestClassifier(numTrees=parameters["example_num_trees"])
    return classifier.fit(training_data)


def predict(model: RandomForestClassifier, testing_data: DataFrame) -> DataFrame:
    """Node for making predictions given a pre-trained model and a testing dataset.
    """
    predictions = model.transform(testing_data)
    return predictions


def report_accuracy(predictions: DataFrame) -> None:
    """Node for reporting the accuracy of the predictions performed by the
    previous node. Notice that this function has no outputs, except logging.
    """
    evaluator = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="accuracy"
    )
    accuracy = evaluator.evaluate(predictions)
    log = logging.getLogger(__name__)
    log.info("Model accuracy: %0.2f%%", accuracy * 100)
