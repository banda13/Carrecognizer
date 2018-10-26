package com.ai.deep.andy.carrecognizer.service;

import android.content.Context;
import android.widget.Toast;

import com.ai.deep.andy.carrecognizer.callbacks.BaseCallback;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;

/**
 * Created by andy on 2018.10.26..
 */

public class CarRecognizer {

    public static final String apiUrl = "https://carrecognizer.herokuapp.com";

    public static void stringRequest(final Context context, final BaseCallback callback){
        StringRequest wakeUpRequest = new StringRequest(Request.Method.GET, apiUrl + "/sorosterv/android/hello",
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        callback.onSuccess(response);
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                callback.onError(error.getMessage());
            }
        });

        MyRequestQueue.getInstance(context).addToRequestQueue(wakeUpRequest);
    }

}
