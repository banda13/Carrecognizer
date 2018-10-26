package com.ai.deep.andy.carrecognizer.callbacks;

/**
 * Created by szabog on 2018.10.26..
 */

public interface BaseCallback {

    void onSuccess(String response);

    void onError(String message);
}
