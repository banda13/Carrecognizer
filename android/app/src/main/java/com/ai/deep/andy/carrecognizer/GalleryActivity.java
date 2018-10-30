package com.ai.deep.andy.carrecognizer;

import android.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import com.ai.deep.andy.carrecognizer.dataModel.Image;
import com.orhanobut.logger.Logger;

public class GalleryActivity extends AppCompatActivity implements GalleryFragment.OnListFragmentInteractionListener{


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gallery);

        GalleryFragment fragment = GalleryFragment.newInstance(1);
        FragmentManager fragmentManager = this.getSupportFragmentManager();
        FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
        fragmentTransaction.add(R.id.container, fragment);
        fragmentTransaction.commit();
    }

    @Override
    public void onListFragmentInteraction(Image item) {
        Logger.i("Katt");
    }
}
