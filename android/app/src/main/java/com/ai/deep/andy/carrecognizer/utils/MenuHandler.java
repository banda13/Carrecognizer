package com.ai.deep.andy.carrecognizer.utils;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.view.Menu;

import com.ai.deep.andy.carrecognizer.GalleryActivity;
import com.ai.deep.andy.carrecognizer.MainActivity;
import com.ai.deep.andy.carrecognizer.R;

public class MenuHandler {

    public static void createOptionsMainMenu(Menu m, Context context){
        ((Activity) context).getMenuInflater().inflate(R.menu.main, m);
    }

    public static void handleNavigationItemSelection(int id, final Context context){
        if (id == R.id.main) {
            Intent i = new Intent(context, MainActivity.class);
            context.startActivity(i);
        } else if (id == R.id.nav_gallery) {
            Intent i = new Intent(context, GalleryActivity.class);
            context.startActivity(i);
        } else if (id == R.id.nav_categories) {

        } else if (id == R.id.nav_tools) {

        }

        DrawerLayout drawer = (DrawerLayout) ((Activity)context).findViewById(R.id.drawer_layout);
        if(drawer != null) {
            drawer.closeDrawer(GravityCompat.START);
        }
    }

}
