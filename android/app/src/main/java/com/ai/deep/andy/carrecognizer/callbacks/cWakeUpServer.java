package com.ai.deep.andy.carrecognizer.callbacks;

import android.content.Context;

import com.ai.deep.andy.carrecognizer.service.CarRecognizer;

/**
 * Created by andy on 2018.10.26..
 */

public class cWakeUpServer {

    private BaseCallback listener;
    private Context context;

    public cWakeUpServer(Context context) {
        this.context = context;
    }

    public BaseCallback getListener() {
        return listener;
    }

    public void setListener(BaseCallback listener) {
        this.listener = listener;
    }

    public void wakeUp(){
        CarRecognizer.stringRequest(context, listener);
    }
}
