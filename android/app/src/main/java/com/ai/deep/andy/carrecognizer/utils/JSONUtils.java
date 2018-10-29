package com.ai.deep.andy.carrecognizer.utils;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by andy on 2018.10.29..
 */

public class JSONUtils {

    public static List<Double> getFloatListFromJSONArray(JSONArray jsonArray) throws JSONException {
        ArrayList<Double> list = new ArrayList<Double>();
        if (jsonArray != null) {
            int len = jsonArray.length();
            for (int i=0;i<len;i++){
                list.add(jsonArray.getDouble(i));
            }
        }
        return list;
    }
}
