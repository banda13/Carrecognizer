from classifiers.cnn2 import Cnn2

#loader = Loader()
#images, labels = loader.load_train_data()
#print(images.shape)
#cnn = Cnn(None, None)
cnn = Cnn2()
cnn.train(continuous_train=True)
#cnn.save()
#cnn.visualize_history()
