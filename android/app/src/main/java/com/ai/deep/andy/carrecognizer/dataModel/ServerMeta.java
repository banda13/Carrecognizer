package com.ai.deep.andy.carrecognizer.dataModel;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.orm.SugarRecord;
import com.orm.dsl.Ignore;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Szabó András on 2018. 10. 30..
 */

public class ServerMeta extends SugarRecord{

    private String version;

    private Double estimatedClassificationTime;

    private Double estimatedWakeupTime;

    @Ignore
    private List<ClassIndex> classIndices = new ArrayList<>();

    private String classIndicesJson;

    public ServerMeta() {
    }

    public String getVersion() {
        return version;
    }

    public void setVersion(String version) {
        this.version = version;
    }

    public Double getEstimatedClassificationTime() {
        return estimatedClassificationTime;
    }

    public void setEstimatedClassificationTime(Double estimatedClassificationTime) {
        this.estimatedClassificationTime = estimatedClassificationTime;
    }

    public Double getEstimatedWakeupTime() {
        return estimatedWakeupTime;
    }

    public void setEstimatedWakeupTime(Double estimatedWakeupTime) {
        this.estimatedWakeupTime = estimatedWakeupTime;
    }

    public List<ClassIndex> getClassIndices() {
        Gson gson = new Gson();
        return gson.fromJson(this.classIndicesJson ,new TypeToken<List<ClassIndex>>(){}.getType());
    }

    public void setClassIndices(List<ClassIndex> classIndices) {
        this.classIndices = classIndices;
        this.classIndicesJson = new Gson().toJson(classIndices);
    }
}
