package com.ai.deep.andy.carrecognizer.dataModel;

import com.orm.SugarRecord;

/**
 * Created by Szabó András on 2018. 10. 30..
 */

public class Prediction extends SugarRecord{

    private Double probability;

    private String label;

    public Prediction() {
    }

    public Prediction(Double prediction, String key) {
        this.probability = prediction;
        this.label = key;
    }

    public Double getProbability() {
        return probability;
    }

    public void setProbability(Double probability) {
        this.probability = probability;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }
}
