package com.ai.deep.andy.carrecognizer.ai;

import android.content.Context;

import com.ai.deep.andy.carrecognizer.dataModel.Image;
import com.ai.deep.andy.carrecognizer.dataModel.Prediction;
import com.ai.deep.andy.carrecognizer.middleware.ClassIndicesMiddleware;
import com.ai.deep.andy.carrecognizer.dataModel.ClassIndex;
import com.ai.deep.andy.carrecognizer.dataModel.DatabaseConstans;
import com.ai.deep.andy.carrecognizer.dataModel.ServerMeta;
import com.ai.deep.andy.carrecognizer.service.Callbacks;
import com.orhanobut.logger.Logger;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;

/**
 * Created by Szabó András on 2018. 10. 30..
 */

public class Classifier {

    private static final Classifier ourInstance = new Classifier();
    public static final Double minPrediction = 0.1;

    private static ServerMeta serverMeta;

    public static Classifier getInstance() {

        if (serverMeta == null) {
            ServerMeta.findById(ServerMeta.class, DatabaseConstans.serverId);
            if(serverMeta != null) {
                Logger.i("Server metadata loaded. Version: " + serverMeta.getVersion());
            }
            else{
                Logger.w("Server meta is null");
            }
        }

        return ourInstance;
    }

    private Classifier() {
    }

    public ServerMeta getServerMeta() {
        return serverMeta;
    }

    public void updateEstimatedClassificationTime(Double classTime){
        serverMeta.setEstimatedClassificationTime(classTime);
        serverMeta.save();
    }

    public void addNewServerVersion(ServerMeta serverMeta, Context context) {
        Logger.i("Setting new server version: " + serverMeta.getVersion());

        ClassIndicesMiddleware classIndicesMiddleware = new ClassIndicesMiddleware(context, new Callbacks.JSONCallback() {
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
                    ClassIndex.deleteAll(ClassIndex.class);
                    try {
                        serverMeta.setClassIndices((List<ClassIndex>) ClassIndex.findAll(ClassIndex.class));
                    } catch (Exception e){
                        Logger.e("Cast exception while converting class indices", e);
                    }
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
        });

        classIndicesMiddleware.call();
        Logger.d("Resolving class indices for new server version started");
    }

    public List<Prediction> getPredictions(JSONArray jsonPredictions) throws JSONException {
        List<Prediction> predictions = new ArrayList<>();;

        for(int i = 0; i < jsonPredictions.getJSONArray(0).length(); i ++){
            Double prediction = jsonPredictions.getJSONArray(0).getDouble(i);

            for(ClassIndex index : serverMeta.getClassIndices()){
                if(index.getCarIndex() == i){
                    predictions.add(new Prediction(prediction, index.getLabel()));
                }
            }
        }

        Collections.sort(predictions,
                (o1, o2) -> o2.getProbability().compareTo(o1.getProbability()));

        Logger.i(predictions.size() + " prediction resolved, biggest probability: " + predictions.get(0).getProbability());
        return predictions;
    }

    public String getTopPredictionsAsString(int limit, List<Prediction> predictions){

        if(predictions.get(0).getProbability() < minPrediction){
            return "I can't recognize it, are you sure it's a car?";
        }

        StringBuilder response = new StringBuilder();
        for(int i = 0; i < limit; i++){
            Prediction pred = predictions.get(i);
            response.append(pred.getLabel()).append(" : ").append(String.format(Locale.ENGLISH, "%.2f", pred.getProbability())).append("\n");
        }
        return response.toString();
    }

}
