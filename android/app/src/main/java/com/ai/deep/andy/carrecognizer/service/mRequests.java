package com.ai.deep.andy.carrecognizer.service;

import android.content.Context;
import android.widget.Toast;

import com.ai.deep.andy.carrecognizer.callbacks.cClassIndices;
import com.ai.deep.andy.carrecognizer.callbacks.cClassify;
import com.ai.deep.andy.carrecognizer.callbacks.cWakeUpServer;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Map;

/**
 * Created by andy on 2018.10.26..
 */

public class mRequests {

    public static final String apiUrl = "https://carrecognizer.herokuapp.com";

    public static void stringRequest(final Context context, final cWakeUpServer.StringCallback callback, String url) {
        StringRequest wakeUpRequest = new StringRequest(Request.Method.GET, apiUrl + url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        callback.onSuccess(response);
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        if(error.getCause() != null) {
                            error.getCause().printStackTrace();
                        }
                        callback.onError(error.getMessage());
                    }
                });

        MyRequestQueue.getInstance(context).addToRequestQueue(wakeUpRequest);
    }

    public static void getJSON(final Context context, final cClassIndices.JsonCallback callback, String url) {
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest
                (Request.Method.GET, apiUrl + url, null, new Response.Listener<JSONObject>() {

                    @Override
                    public void onResponse(JSONObject response) {
                        callback.onSuccess(response);
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        error.getCause().printStackTrace();
                        callback.onError(error.getMessage());
                    }
                });
        MyRequestQueue.getInstance(context).addToRequestQueue(jsonObjectRequest);
    }

    public static void postImage(final Context context, String imagePath, String url, final cClassify.ClassificationCallback callback) {
        /*SimpleMultiPartRequest smr = new SimpleMultiPartRequest(Request.Method.POST, apiUrl + url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try {
                            JSONObject jObj = new JSONObject(response);
                            callback.onSuccess(jObj);
                        } catch (JSONException e) {
                            e.printStackTrace();
                            callback.onError("json error");
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                callback.onError(error.getMessage());
            }
        });
        smr.addFile("image", imagePath);
        MyRequestQueue.getInstance(context).addToRequestQueue(smr);*/
        Toast.makeText(context, "Oopsie", Toast.LENGTH_SHORT).show();
    }


}
