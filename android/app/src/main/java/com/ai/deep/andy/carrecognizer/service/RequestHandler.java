package com.ai.deep.andy.carrecognizer.service;

import android.content.Context;
import android.graphics.Bitmap;

import com.ai.deep.andy.carrecognizer.utils.ImageUtils;
import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.orhanobut.logger.Logger;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by andy on 2018.10.26..
 */

public class RequestHandler {

    public static void stringRequest(final Context context, final Callbacks.StringCallback callback, String url) {
        Logger.t("REQUEST").d("String request for: " + url);
        StringRequest wakeUpRequest = new StringRequest(Request.Method.GET, url,
                callback::onSuccess,
                error -> {
                    Logger.e("Volley error in string request", error.getCause());
                    callback.onError(error.getMessage());
                });

        MyRequestQueue.getInstance(context).addToRequestQueue(wakeUpRequest);
    }

    public static void jsonRequest(final Context context, final Callbacks.JSONCallback callback, String url) {
        Logger.t("REQUEST").d("JSON request for: " + url);
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest
                (Request.Method.GET, url, null,
                        callback::onSuccess,
                        error -> {
                            Logger.e("Volley error in json request", error.getCause());
                            callback.onError(error.getMessage());
                        });
        MyRequestQueue.getInstance(context).addToRequestQueue(jsonObjectRequest);
    }

    public static void multipartPostRequest(final Context context, final Bitmap bitmap, String url, Callbacks.JSONCallback listener) {
        Logger.t("REQUEST").d("Multipart post request for: " + url);
        VolleyMultipartRequest volleyMultipartRequest = new VolleyMultipartRequest(Request.Method.POST, url,
                response -> {
                    try {
                        JSONObject obj = new JSONObject(new String(response.data));
                        listener.onSuccess(obj);
                    } catch (JSONException e) {
                        Logger.e("Json processing error in multipart post request", e);
                        listener.onError("Json error");
                    }
                },
                error -> {
                    Logger.e("Volley error in multipart post request", error.getCause());
                    listener.onError(error.getMessage());
                }) {

            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                Map<String, String> params = new HashMap<>();
                //params.put("tags", tags);
                return params;
            }


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

}
