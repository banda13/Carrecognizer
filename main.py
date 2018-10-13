from classifiers.cnn3 import Cnn3
from random import sample
import os

from classifiers.cnn_test import cnn3_test


def test():
    paths = ["data/hasznaltauto/bmw/", "data/hasznaltauto/ford/", "data/hasznaltauto/mercedes/",
             "data/hasznaltauto/volkswagen/"]

    for path in paths:
        for car in sample(os.listdir(path), 3):
            Cnn3("e7247c4f-88c1-4f0d-bf62-f7850de6d949").predict(path + car, car)


#cnn = Cnn3("e7247c4f-88c1-4f0d-bf62-f7850de6d949")
#cnn.model_to_graph()
#cnn.print_graph_nodes("model/bottleneck_graph.pb")

#cnn = Cnn3()
#cnn.save_bottlebeck_features()
#cnn.train_top_model()
#cnn.model_to_graph()


cnn = Cnn3()
# cnn.save_bottlebeck_features()
tezt = cnn3_test()
tezt.setup_models()
tezt.run_tests()
