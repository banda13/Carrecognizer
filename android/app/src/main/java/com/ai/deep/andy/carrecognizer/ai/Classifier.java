package com.ai.deep.andy.carrecognizer.ai;

import android.content.Context;

import com.ai.deep.andy.carrecognizer.middleware.ClassIndicesMiddleware;
import com.ai.deep.andy.carrecognizer.dataModel.ClassIndex;
import com.ai.deep.andy.carrecognizer.dataModel.DatabaseConstans;
import com.ai.deep.andy.carrecognizer.dataModel.ServerMeta;
import com.ai.deep.andy.carrecognizer.service.Callbacks;
import com.orhanobut.logger.Logger;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Iterator;

/**
 * Created by Szabó András on 2018. 10. 30..
 */

public class Classifier {

    private static final Classifier ourInstance = new Classifier();

    private static ServerMeta serverMeta;

    public static Classifier getInstance() {

        if (serverMeta == null) {
            ServerMeta.findById(ServerMeta.class, DatabaseConstans.serverId);
            Logger.i("Server metadata loaded. Version: " + serverMeta.getVersion());
        }

        return ourInstance;
    }

    private Classifier() {
    }

    public ServerMeta getServerMeta() {
        return serverMeta;
    }

    public void addNewServerVersion(ServerMeta serverMeta, Context context) {
        Logger.i("Setting new server version: " + serverMeta.getVersion());

        ClassIndicesMiddleware classIndicesResolver = new ClassIndicesMiddleware(context, new Callbacks.JSONCallback() {
            @Override
            public void onSuccess(JSONObject classIndices) {
                try {
                    Iterator<String> keys = classIndices.keys();
                    int deleted = ClassIndex.deleteAll(ClassIndex.class);
                    Logger.i(deleted + " old class indices were deleted");
                    int newIndices = 0;
                    while (keys.hasNext()) {
                        String key = keys.next();
                        int id = 0;
                        id = classIndices.getInt(key);
                        ClassIndex index = new ClassIndex(key, id);
                        index.save();
                        newIndices ++;
                    }
                    serverMeta.setClassIndices(ClassIndex.findAll(ClassIndex.class));
                    Logger.i(newIndices + " new index saved");

                    Classifier.serverMeta = serverMeta;
                    serverMeta.setId(DatabaseConstans.serverId);
                    ServerMeta.save(serverMeta);
                    Logger.i("Setting new server version was successful: " + serverMeta.getVersion());
                } catch (JSONException e) {
                    Logger.e("Failed to set new server version due to JSONException", e);
                }
            }

            @Override
            public void onError(String message) {
                Logger.e("New server version was not set: " + message);
            }
        }).use();

        Logger.d("Resolving class indices for new server version started");
    }
}
