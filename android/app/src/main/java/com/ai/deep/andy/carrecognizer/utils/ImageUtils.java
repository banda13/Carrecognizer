package com.ai.deep.andy.carrecognizer.utils;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.Paint;

public class ImageUtils {

    public static Bitmap getCroppedBitmap(Bitmap bitmap){
        Bitmap croppedBitmap = Bitmap.createBitmap(224, 224, Bitmap.Config.ARGB_8888);
        Matrix transformationMatrix = getPhotoBitmapTransformationMatrix(bitmap);
        Canvas canvas = new Canvas(croppedBitmap);
        canvas.drawBitmap(bitmap, transformationMatrix, null);
        return croppedBitmap;
    }

    private static final Matrix getPhotoBitmapTransformationMatrix(Bitmap bitmap) {
        Matrix frameToCropTransformationMatrix = getTransformationMatrix(bitmap.getWidth(), bitmap.getHeight(), 224, 224, 0, true);
        Matrix cropToFrameTransformationMatrix = new Matrix();
        frameToCropTransformationMatrix.invert(cropToFrameTransformationMatrix);
        return frameToCropTransformationMatrix;
    }

    private static final Matrix getTransformationMatrix(int srcWidth, int srcHeight, int dstWidth, int dstHeight, int applyRotation, boolean maintainAspectRatio) {
        Matrix matrix = new Matrix();
        matrix.postTranslate((float)(-srcWidth) / 2.0F, (float)(-srcHeight) / 2.0F);
        matrix.postRotate((float)applyRotation);
        boolean transpose = (Math.abs(applyRotation) + 90) % 180 == 0;
        int inWidth = transpose ? srcHeight : srcWidth;
        int inHeight = transpose ? srcWidth : srcHeight;
        if (inWidth != dstWidth || inHeight != dstHeight) {
            float scaleFactorX = (float)dstWidth / (float)inWidth;
            float scaleFactorY = (float)dstHeight / (float)inHeight;
            if (maintainAspectRatio) {
                float scaleFactor = Math.max(scaleFactorX, scaleFactorY);
                matrix.postScale(scaleFactor, scaleFactor);
            } else {
                matrix.postScale(scaleFactorX, scaleFactorY);
            }
        }

        matrix.postTranslate((float)dstWidth / 2.0F, (float)dstHeight / 2.0F);
        return matrix;
    }
}
