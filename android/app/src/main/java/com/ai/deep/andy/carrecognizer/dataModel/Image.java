package com.ai.deep.andy.carrecognizer.dataModel;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.ParcelFileDescriptor;

import com.ai.deep.andy.carrecognizer.utils.FileUtils;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.orhanobut.logger.Logger;
import com.orm.SugarRecord;
import com.orm.dsl.Ignore;

import java.io.FileDescriptor;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * Created by Szabó András on 2018. 10. 30..
 */

public class Image extends SugarRecord{

    private String path;

    @Ignore
    private Bitmap bitmap;

    private Date captured;

    @Ignore
    private List<Prediction> predictions  = new ArrayList<>();

    private String mainPrediction;

    private String predictionJson;

    private Date lastClassificationDate;

    private String serverVersion;

    private Double classificationDuration;

    private String classificationId;

    public Image() {
    }

    public Image(final Context context, Uri uri){
        ParcelFileDescriptor parcelFileDescriptor =
                null;
        try {
            parcelFileDescriptor = context.getContentResolver().openFileDescriptor(uri, "r");

            FileDescriptor fileDescriptor = parcelFileDescriptor.getFileDescriptor();
            bitmap = BitmapFactory.decodeFileDescriptor(fileDescriptor);
            parcelFileDescriptor.close();

            path = FileUtils.getPath(context, uri);
            captured = new Date();

            Logger.i("Image create from uri: " + uri.getPath());
        } catch (FileNotFoundException e) {
            Logger.e("Cannot create image from URI: " + uri.getPath(), e);
        } catch (IOException e) {
            Logger.e("Cannot create image from URI: " + uri.getPath(), e);
        }
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public Bitmap getBitmap() {
        return bitmap;
    }

    public void setBitmap(Bitmap bitmap) {
        this.bitmap = bitmap;
    }

    public Date getCaptured() {
        return captured;
    }

    public void setCaptured(Date captured) {
        this.captured = captured;
    }

    public List<Prediction> getPredictions() {
        Gson gson = new Gson();
        return gson.fromJson(this.predictionJson,new TypeToken<List<Prediction>>(){}.getType());
    }

    public void setPredictions(List<Prediction> predictions) {
        this.predictions = predictions;
        this.predictionJson = new Gson().toJson(predictions);
    }

    public String getPredictionJson() {
        return predictionJson;
    }

    public void setPredictionJson(String predictionJson) {
        this.predictionJson = predictionJson;
    }

    public Date getLastClassificationDate() {
        return lastClassificationDate;
    }

    public void setLastClassificationDate(Date lastClassificationDate) {
        this.lastClassificationDate = lastClassificationDate;
    }

    public String getServerVersion() {
        return serverVersion;
    }

    public void setServerVersion(String serverVersion) {
        this.serverVersion = serverVersion;
    }

    public Double getClassificationDuration() {
        return classificationDuration;
    }

    public void setClassificationDuration(Double classificationDuration) {
        this.classificationDuration = classificationDuration;
    }

    public String getClassificationId() {
        return classificationId;
    }

    public void setClassificationId(String classificationId) {
        this.classificationId = classificationId;
    }

    public String getMainPrediction() {
        return mainPrediction;
    }

    public void setMainPrediction(String mainPrediction) {
        this.mainPrediction = mainPrediction;
    }

    public void setClassificationResults(String serverVersion, Double classificationDuration, String classificationId, List<Prediction> predictions){
        this.lastClassificationDate = new Date();
        this.classificationDuration = classificationDuration;
        this.serverVersion = serverVersion;
        this.classificationId = classificationId;
        this.predictions = predictions;
    }

}
