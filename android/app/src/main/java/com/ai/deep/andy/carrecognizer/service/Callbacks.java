package com.ai.deep.andy.carrecognizer.service;

import org.json.JSONObject;

/**
 * Created by Szabó András on 2018. 10. 30..
 */

public class Callbacks {

    public interface AbstractCallback{}

    public interface StringCallback extends AbstractCallback{

        void onSuccess(String response);

        void onError(String message);
    }

    public interface JSONCallback extends AbstractCallback{

        void onSuccess(JSONObject response);

        void onError(String message);
    }
}
