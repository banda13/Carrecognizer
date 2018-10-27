package com.ai.deep.andy.carrecognizer.callbacks;

import android.content.Context;
import android.graphics.Bitmap;
import android.widget.Toast;

import com.ai.deep.andy.carrecognizer.service.mRequests;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by andy on 2018.10.26..
 */

public class cClassify{

    private static final String CLASSIFICATION_URL = "/classify";
    private ClassificationCallback listener;
    private Context context;

    public cClassify(Context context) {
        this.context = context;
    }

    public ClassificationCallback getListener() {
        return listener;
    }

    public void setListener(ClassificationCallback listener) {
        this.listener = listener;
    }

    public byte[] getFileDataFromDrawable(Bitmap bitmap) {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 80, byteArrayOutputStream);
        return byteArrayOutputStream.toByteArray();
    }

    public void classifyimage(String imagePath){
        mRequests.postImage(context, imagePath, CLASSIFICATION_URL, this.listener);
    }

    public interface ClassificationCallback extends cClassIndices.JsonCallback {

        @Override
        void onSuccess(JSONObject response);

        @Override
        void onError(String message);
    }
}
