package com.ai.deep.andy.carrecognizer.callbacks;

import org.json.JSONObject;

/**
 * Created by andy on 2018.10.26..
 */

public class cClassIndices {

    private JsonCallback listener;

    public cClassIndices() {
    }

    public JsonCallback getListener() {
        return listener;
    }

    public void setListener(JsonCallback listener) {
        this.listener = listener;
    }

    public interface JsonCallback {

        void onSuccess(JSONObject response);

        void onError(String message);
    }
}
