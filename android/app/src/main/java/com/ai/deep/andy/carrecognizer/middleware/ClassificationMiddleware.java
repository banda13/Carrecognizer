package com.ai.deep.andy.carrecognizer.middleware;

import android.content.Context;
import android.graphics.Bitmap;

import com.ai.deep.andy.carrecognizer.service.Callbacks;
import com.ai.deep.andy.carrecognizer.service.EndpointURL;
import com.ai.deep.andy.carrecognizer.service.MyRequestQueue;
import com.ai.deep.andy.carrecognizer.service.RequestHandler;
import com.ai.deep.andy.carrecognizer.service.VolleyMultipartRequest;
import com.ai.deep.andy.carrecognizer.utils.ImageUtils;
import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.orhanobut.logger.Logger;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by andy on 2018.10.26..
 */

public class ClassificationMiddleware extends AbstractMiddleware{

    public ClassificationMiddleware(Context context, Callbacks.JSONCallback listener) {
        super(context, listener);
    }

    protected void call(Bitmap bitmap) {
        Logger.i("Classifying image started");
        RequestHandler.multipartPostRequest(context, bitmap, EndpointURL.CLASSIFICATION_URL, (Callbacks.JSONCallback) listener);
    }
}
