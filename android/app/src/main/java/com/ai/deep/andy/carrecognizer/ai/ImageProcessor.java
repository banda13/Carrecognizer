package com.ai.deep.andy.carrecognizer.ai;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.ParcelFileDescriptor;
import android.util.Log;
import android.widget.Toast;

import com.ai.deep.andy.carrecognizer.callbacks.cClassIndices;
import com.ai.deep.andy.carrecognizer.utils.Constants;
import com.ai.deep.andy.carrecognizer.utils.FileUtils;

import org.json.JSONObject;

import java.io.FileDescriptor;
import java.io.FileNotFoundException;
import java.io.IOException;

public class ImageProcessor {

    private Bitmap image;
    private String imagePath;

    private JSONObject classIndices;

    public Bitmap getImage() {
        return image;
    }

    public void setImage(Bitmap image) {
        this.image = image;
    }

    public String getImagePath() {
        return imagePath;
    }

    public void setImagePath(String imagePath) {
        this.imagePath = imagePath;
    }

    public JSONObject getClassIndices() {
        return classIndices;
    }

    public void setClassIndices(JSONObject classIndices) {
        this.classIndices = classIndices;
    }

    public void setImageFromUri(final Context context, Uri uri){
        final ImageProcessor thiz = this;
        // TODO refactor class infices resolver
        cClassIndices classIndicesResolver = new cClassIndices(context);
        classIndicesResolver.setListener(new cClassIndices.JsonCallback() {
            @Override
            public void onSuccess(JSONObject response) {
                Toast.makeText(context, "Class indices resolved..", Toast.LENGTH_SHORT).show();
                thiz.classIndices = response;
            }

            @Override
            public void onError(String message) {
                Toast.makeText(context, "Failed to resolve class indices", Toast.LENGTH_SHORT).show();
            }
        });
        classIndicesResolver.queryClassIndices();
        ParcelFileDescriptor parcelFileDescriptor =
                null;
        try {
            parcelFileDescriptor = context.getContentResolver().openFileDescriptor(uri, "r");

            FileDescriptor fileDescriptor = parcelFileDescriptor.getFileDescriptor();
            image = BitmapFactory.decodeFileDescriptor(fileDescriptor);
            parcelFileDescriptor.close();

            imagePath = FileUtils.getPath(context, uri);

            Log.i(Constants.LogTag, "Image set");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}
