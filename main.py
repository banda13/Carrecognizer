from classifiers.cnn2 import Cnn2

#loader = Loader()
#images, labels = loader.load_train_data()
#print(images.shape)
#cnn = Cnn(None, None)
from test import manual_accuracy_test, safer_manual_accuracy_test

cnn = Cnn2()
cnn.load()
#cnn.train()
#cnn.save()
#cnn.visualize_history()

safer_manual_accuracy_test(cnn)
