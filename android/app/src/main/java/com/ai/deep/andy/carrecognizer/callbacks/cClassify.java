package com.ai.deep.andy.carrecognizer.callbacks;

import org.json.JSONObject;

/**
 * Created by szabog on 2018.10.26..
 */

public class cClassify{

    private ClassificationCallback listener;

    public cClassify() {
    }

    public ClassificationCallback getListener() {
        return listener;
    }

    public void setListener(ClassificationCallback listener) {
        this.listener = listener;
    }

    public interface ClassificationCallback extends cClassIndices.JsonCallback {

        @Override
        void onSuccess(JSONObject response);

        @Override
        void onError(String message);
    }
}
