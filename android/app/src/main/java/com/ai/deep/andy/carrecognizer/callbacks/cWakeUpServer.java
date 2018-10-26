package com.ai.deep.andy.carrecognizer.callbacks;

import android.content.Context;

import com.ai.deep.andy.carrecognizer.service.mRequests;

/**
 * Created by andy on 2018.10.26..
 */

public class cWakeUpServer {

    private StringCallback listener;
    private Context context;
    private String url = "/sorosterv/android/hello";

    public cWakeUpServer(Context context) {
        this.context = context;
    }

    public StringCallback getListener() {
        return listener;
    }

    public void setListener(StringCallback listener) {
        this.listener = listener;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public void wakeUp(){
        mRequests.stringRequest(context, listener, url);
    }

    public interface StringCallback{

        void onSuccess(String response);

        void onError(String message);
    }
}
