package com.ai.deep.andy.carrecognizer.middleware;

import android.content.Context;

import com.ai.deep.andy.carrecognizer.service.Callbacks;
import com.orhanobut.logger.Logger;

/**
 * Created by Szabó András on 2018. 10. 30..
 */

public abstract class AbstractMiddleware {

    protected Context context;

    protected Callbacks.AbstractCallback listener;

    AbstractMiddleware(Context context, Callbacks.AbstractCallback listener) {
        this.context = context;
        this.listener = listener;
        Logger.d("Middleware initialized");
    }

    public Callbacks.AbstractCallback getListener() {
        return listener;
    }

    public void setListener(Callbacks.AbstractCallback listener) {
        this.listener = listener;
    }

    public Context getContext() {
        return context;
    }

    public void setContext(Context context) {
        this.context = context;
    }
}
