package com.ai.deep.andy.carrecognizer.dataModel;

import com.orm.SugarRecord;

import java.util.List;

/**
 * Created by Szabó András on 2018. 10. 30..
 */

public class ClassIndex extends SugarRecord{

    private String label;

    private int carIndex;

    public ClassIndex(String label, int id) {
        this.label = label;
        this.carIndex = id;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public int getCarIndex() {
        return carIndex;
    }

    public void setCarIndex(int carIndex) {
        this.carIndex = carIndex;
    }
}
