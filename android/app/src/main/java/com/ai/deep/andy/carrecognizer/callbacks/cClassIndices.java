package com.ai.deep.andy.carrecognizer.callbacks;

import android.content.Context;

import com.ai.deep.andy.carrecognizer.service.mRequests;

import org.json.JSONObject;

/**
 * Created by andy on 2018.10.26..
 */

public class cClassIndices {

    private static String url = "/classindices";
    private JsonCallback listener;
    private Context context;

    public cClassIndices(Context context) {
        this.context = context;
    }

    public JsonCallback getListener() {
        return listener;
    }

    public void setListener(JsonCallback listener) {
        this.listener = listener;
    }

    public void queryClassIndices(){
        mRequests.getJSON(context, this.listener, url);
    }

    public interface JsonCallback {

        void onSuccess(JSONObject response);

        void onError(String message);
    }
}
