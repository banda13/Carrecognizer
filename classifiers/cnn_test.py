from keras.engine.saving import load_model


class TestCNN(object):

    def __init__(self, pid, params):
        self.pid = pid
        self.model_path = params['model']
        self.test_count_per_class = params['test_count_per_class']
        self.accuracy = params['accuracy']
        self.category_results = params['category_results']
        self.data_source_dirs = params['data_source_dirs']

        print("TestCNN initialized")

    def test(self):
        print("Testing CNN started..")

        model = load_model(self.model_path)
        print("Model loaded")


