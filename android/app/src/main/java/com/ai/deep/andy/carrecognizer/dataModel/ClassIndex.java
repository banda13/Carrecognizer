package com.ai.deep.andy.carrecognizer.dataModel;

import com.orm.SugarRecord;

/**
 * Created by Szabó András on 2018. 10. 30..
 */

public class ClassIndex extends SugarRecord{

    private String label;

    private int index;

    public ClassIndex(String label, int id) {
        this.label = label;
        this.index = id;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
    }

    public int getIndex() {
        return index;
    }

    public void setIndex(int index) {
        this.index = index;
    }
}
