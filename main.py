from classifiers.cnn2 import Cnn2

#loader = Loader()
#images, labels = loader.load_train_data()
#print(images.shape)
#cnn = Cnn(None, None)
print("mi van veled python..")
cnn = Cnn2()
cnn.train()
cnn.save()
cnn.visualize_history()
