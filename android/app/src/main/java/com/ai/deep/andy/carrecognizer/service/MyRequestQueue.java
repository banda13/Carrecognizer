package com.ai.deep.andy.carrecognizer.service;

import android.annotation.SuppressLint;
import android.content.Context;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.ImageLoader;
import com.android.volley.toolbox.Volley;

/**
 * Created by andy on 2018.10.26..
 */

@SuppressLint("StaticFieldLeak")
public class MyRequestQueue {

    private static MyRequestQueue ourInstance;
    private RequestQueue mRequestQueue;
    private static Context mCtx;

    private static final int MY_SOCKET_TIMEOUT_MS = 30000;

    static synchronized MyRequestQueue getInstance(Context context) {
        if (ourInstance == null) {
            ourInstance = new MyRequestQueue(context);
        }
        return ourInstance;
    }

    private MyRequestQueue(Context context) {
        mCtx = context;
        mRequestQueue = getRequestQueue();
    }

    private RequestQueue getRequestQueue() {
        if (mRequestQueue == null) {
            // getApplicationContext() is key, it keeps you from leaking the
            // Activity or BroadcastReceiver if someone passes one in.
            mRequestQueue = Volley.newRequestQueue(mCtx.getApplicationContext());
        }
        return mRequestQueue;
    }

    <T> void addToRequestQueue(Request<T> req) {
        req.setRetryPolicy(new DefaultRetryPolicy(
                MY_SOCKET_TIMEOUT_MS,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

        getRequestQueue().add(req);
    }
}
