package com.ai.deep.andy.carrecognizer.utils;

import android.content.Context;
import android.content.res.AssetManager;
import android.database.Cursor;
import android.net.Uri;
import android.provider.MediaStore;
import android.support.v4.content.CursorLoader;

public class FileUtils {

    public static String[] getLabels(AssetManager assets, String filepath){
        //TODO
        return new String[] {"bmw", "ford", "mercedes", "volkswagen"};
    }

    // Get Path of selected image
    private String getPath(Context c, Uri contentUri) {
        String[] proj = { MediaStore.Images.Media.DATA };
        CursorLoader loader = new CursorLoader(c,    contentUri, proj, null, null, null);
        Cursor cursor = loader.loadInBackground();
        int column_index = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
        cursor.moveToFirst();
        String result = cursor.getString(column_index);
        cursor.close();
        return result;
    }
}
