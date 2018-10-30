package com.ai.deep.andy.carrecognizer.ai;
import android.content.Context;
import android.graphics.Bitmap;
import android.util.Log;

import com.ai.deep.andy.carrecognizer.utils.FileUtils;
import com.ai.deep.andy.carrecognizer.utils.ImageUtils;

import org.tensorflow.contrib.android.TensorFlowInferenceInterface;

/*
 This is the implementation of server side tensorflow classification
 Currently disabled because the size of the models
 But it's much faster than server side classification
 */

@Deprecated
public class OldClassifier {

    private static final String LABELS_FILE = "file:///android_asset/labels.txt";
    private static final int imageSize = 224;
    private static final int NUM_CHANGELS = 3;

    private static final String BOTTLENECK_MODEL_PATH = "file:///android_asset/bottleneck_graph.pb";
    private static final String BOTTLENECK_INPUT_NODES = "input_1";
    private static final String BOTTLENECK_OUTPUT_NODES = "block5_pool/MaxPool";

    private static final String TOP_MODEL_PATH = "file:///android_asset/top_graph.pb";
    private static final String TOP_INPUT_NODES = "flatten_1_input";
    private static final String TOP_OUTPUT_NODES = "dense_2/Softmax";

    private static int [] imageBitmapPixels = new int[imageSize * imageSize];
    private static float [] imageNormalizedPixels =  new float[imageSize * imageSize * NUM_CHANGELS];
    private static float[] results = new float[7*7*512];
    private static float[] results2 = new float[4];


    public static String classify(Context context, Bitmap image){
        TensorFlowInferenceInterface bottleneck_model = new TensorFlowInferenceInterface(context.getAssets(), BOTTLENECK_MODEL_PATH);
        TensorFlowInferenceInterface top_model = new TensorFlowInferenceInterface(context.getAssets(), TOP_MODEL_PATH);

        Bitmap croppedBitmap = ImageUtils.getCroppedBitmap(image);
        preProcessImage(croppedBitmap);

        String[] labels = FileUtils.getLabels(context.getAssets(), LABELS_FILE);

        bottleneck_model.feed(BOTTLENECK_INPUT_NODES, imageNormalizedPixels, 1L, imageSize, imageSize, NUM_CHANGELS);
        bottleneck_model.run(new String[] {BOTTLENECK_OUTPUT_NODES}, false);
        bottleneck_model.fetch(BOTTLENECK_OUTPUT_NODES, results);

        float[][] asd = new float[3][3];
        top_model.feed(TOP_INPUT_NODES, results, 1L, 7, 7,  512);
        top_model.run(new String[] {TOP_INPUT_NODES}, false);
        top_model.fetch(TOP_OUTPUT_NODES, results2);

        return "juppi";
    }

    private static  void preProcessImage(Bitmap bitmap){
        int imageMean = 128;
        float imageStd = 128.0f;
        bitmap.getPixels(imageBitmapPixels, 0, bitmap.getWidth(), 0, 0, bitmap.getWidth(), bitmap.getHeight());

        for(int i = 0; i < imageBitmapPixels.length; i++){
            int pix = imageBitmapPixels[i];
            imageNormalizedPixels[i * 3 + 0] = (float)((pix >> 16 & 255) - imageMean) / imageStd;
            imageNormalizedPixels[i * 3 + 1] = (float)((pix >> 8 & 255) - imageMean) / imageStd;
            imageNormalizedPixels[i * 3 + 2] = (float)((pix & 255) - imageMean) / imageStd;
        }
    }
}
