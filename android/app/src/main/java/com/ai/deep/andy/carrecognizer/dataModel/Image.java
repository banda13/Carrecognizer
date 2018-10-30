package com.ai.deep.andy.carrecognizer.dataModel;

import android.graphics.Bitmap;

import com.orm.SugarRecord;
import com.orm.dsl.Ignore;

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

    private List<Prediction> predictions;

    private Date lastClassificationDate;

    private String serverVersion;

    private Double classificationDuration;

    private String classificationId;

    public Image() {
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
        return predictions;
    }

    public void setPredictions(List<Prediction> predictions) {
        this.predictions = predictions;
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
}
