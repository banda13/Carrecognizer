package com.ai.deep.andy.carrecognizer.callbacks;

import android.content.Context;
import android.graphics.Bitmap;
import android.widget.Toast;

import com.ai.deep.andy.carrecognizer.service.MyRequestQueue;
import com.ai.deep.andy.carrecognizer.service.VolleyMultipartRequest;
import com.ai.deep.andy.carrecognizer.service.mRequests;
import com.ai.deep.andy.carrecognizer.utils.ImageUtils;
import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by andy on 2018.10.26..
 */

public class cClassify{

    private static final String CLASSIFICATION_URL = "https://carrecognizer.herokuapp.com/classify";
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

    // TODO endpoints . Uploadurl etc
    public void classifyimage(final Bitmap bitmap){
        //mRequests.postImage(context, imagePath, CLASSIFICATION_URL, this.listener);

        VolleyMultipartRequest volleyMultipartRequest = new VolleyMultipartRequest(Request.Method.POST, CLASSIFICATION_URL,
                new Response.Listener<NetworkResponse>() {
                    @Override
                    public void onResponse(NetworkResponse response) {
                        try {
                            JSONObject obj = new JSONObject(new String(response.data));
                            listener.onSuccess(obj);
                        } catch (JSONException e) {
                            e.printStackTrace();
                            listener.onError("Json error");
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        listener.onError(error.getMessage());
                    }
                }) {

            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                Map<String, String> params = new HashMap<>();
                //params.put("tags", tags);
                return params;
            }

            /*
             * Here we are passing image by renaming it with a unique name
             * */
            @Override
            protected Map<String, DataPart> getByteData() {
                Map<String, DataPart> params = new HashMap<>();
                long imagename = System.currentTimeMillis();
                params.put("file", new DataPart(imagename + ".png", ImageUtils.getFileDataFromDrawable(bitmap)));
                return params;
            }
        };

        MyRequestQueue.getInstance(context).addToRequestQueue(volleyMultipartRequest);
    }

    public interface ClassificationCallback extends cClassIndices.JsonCallback {

        @Override
        void onSuccess(JSONObject response);

        @Override
        void onError(String message);
    }
}
