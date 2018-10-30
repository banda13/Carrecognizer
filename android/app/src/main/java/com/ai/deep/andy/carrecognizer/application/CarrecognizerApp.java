package com.ai.deep.andy.carrecognizer.application;

import com.orhanobut.logger.AndroidLogAdapter;
import com.orhanobut.logger.FormatStrategy;
import com.orhanobut.logger.PrettyFormatStrategy;
import com.orm.SugarApp;

/**
 * Created by Szabó András on 2018. 10. 29..
 */

public class CarrecognizerApp extends SugarApp {

    private static final String LOG_TAG = "CAR_AI";

    @Override
    public void onCreate() {
        super.onCreate();

        FormatStrategy formatStrategy = PrettyFormatStrategy.newBuilder()
                //.showThreadInfo(false)  // (Optional) Whether to show thread info or not. Default true
                //.methodCount(0)         // (Optional) How many method line to show. Default 2
                //.methodOffset(3)        // (Optional) Skips some method invokes in stack trace. Default 5
                .tag(LOG_TAG)   // (Optional) Custom tag for each log. Default PRETTY_LOGGER
                .build();

        com.orhanobut.logger.Logger.addLogAdapter(new AndroidLogAdapter(formatStrategy));
    }
}
