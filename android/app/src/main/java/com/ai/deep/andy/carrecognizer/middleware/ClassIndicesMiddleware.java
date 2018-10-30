package com.ai.deep.andy.carrecognizer.middleware;

import android.content.Context;

import com.ai.deep.andy.carrecognizer.service.Callbacks;
import com.ai.deep.andy.carrecognizer.service.EndpointURL;
import com.ai.deep.andy.carrecognizer.service.RequestHandler;
import com.orhanobut.logger.Logger;

/**
 * Created by andy on 2018.10.26..
 */

public class ClassIndicesMiddleware extends AbstractMiddleware{

    public ClassIndicesMiddleware(Context context, Callbacks.JSONCallback listener) {
        super(context, listener);
    }

    public void call(){
        Logger.d("Querying class indices started");
        RequestHandler.jsonRequest(context, (Callbacks.JSONCallback) this.listener, EndpointURL.CLASS_INDICES);
    }

}
