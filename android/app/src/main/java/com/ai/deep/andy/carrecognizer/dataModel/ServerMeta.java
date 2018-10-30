package com.ai.deep.andy.carrecognizer.dataModel;

import com.orm.SugarRecord;

import java.util.List;

/**
 * Created by Szabó András on 2018. 10. 30..
 */

public class ServerMeta extends SugarRecord{

    private String version;

    private Double estimatedClassificationTime;

    private Double estimatedWakeupTime;

    private List<ClassIndex> classIndices;

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
        return classIndices;
    }

    public void setClassIndices(List<ClassIndex> classIndices) {
        this.classIndices = classIndices;
    }
}
