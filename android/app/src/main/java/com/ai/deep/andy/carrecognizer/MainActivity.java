package com.ai.deep.andy.carrecognizer;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.ai.deep.andy.carrecognizer.ai.ImageProcessor;
import com.ai.deep.andy.carrecognizer.callbacks.cClassify;
import com.ai.deep.andy.carrecognizer.callbacks.cWakeUpServer;
import com.ai.deep.andy.carrecognizer.model.Prediction;
import com.ai.deep.andy.carrecognizer.utils.FileUtils;
import com.orhanobut.logger.Logger;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    private static int RESULT_LOAD_IMAGE = 1;
    private static final int CAMERA_PERMISSION_CODE = 100;
    private static final int WRITE_EXTERAL_PERMISSION_CODE = 101;
    private static final int CAMERA_REQUEST = 1888;

    private FloatingActionButton camera;
    private FloatingActionButton gallery;
    private ImageView imageView;
    private ProgressBar serverLoading;
    private ImageView serverOnline;
    private ImageView serverOffline;
    private RelativeLayout mainLayout;
    private ImageButton classifyButton;
    private TextView classificationResult;
    private ProgressBar classificationProgress;
    private DrawerLayout drawer;

    private ImageProcessor imageProcessor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        camera = findViewById(R.id.camera);
        gallery = findViewById(R.id.gallery);
        imageView = findViewById(R.id.imgView);
        serverLoading = findViewById(R.id.serverLoading);
        serverOnline = findViewById(R.id.serverOnline);
        serverOffline = findViewById(R.id.serverOfflie);
        mainLayout = findViewById(R.id.main_layout);
        classifyButton = findViewById(R.id.classify);
        classificationResult = findViewById(R.id.classificationResult);
        classificationProgress = findViewById(R.id.classificationProgress);

        final Context context = this;
        checkServerAvailability(context);

        gallery.setOnClickListener(new View.OnClickListener() {

                @Override
                public void onClick(View arg0) {
                    Logger.d("Opening gallery");
                    Intent i = new Intent(
                            Intent.ACTION_PICK,
                            android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);

                    startActivityForResult(i, RESULT_LOAD_IMAGE);
                }
        });

        camera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    if (checkSelfPermission(Manifest.permission.CAMERA)
                            != PackageManager.PERMISSION_GRANTED || checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                            != PackageManager.PERMISSION_GRANTED ) {
                        if((checkSelfPermission(Manifest.permission.CAMERA)
                                != PackageManager.PERMISSION_GRANTED)){
                            Logger.d("Requesting camera permission..");
                            requestPermissions(new String[]{Manifest.permission.CAMERA},
                                    CAMERA_PERMISSION_CODE);
                        }
                        if((checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                                != PackageManager.PERMISSION_GRANTED)){
                            Logger.d("Requesting ");
                            requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE},
                                    CAMERA_PERMISSION_CODE);
                        }
                    } else {
                        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                        startActivityForResult(cameraIntent, CAMERA_REQUEST);
                    }
                }
                else{
                    Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                    startActivityForResult(cameraIntent, CAMERA_REQUEST);
                }
            }

        });

        classifyButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                if(imageProcessor == null || imageProcessor.getImage() == null){
                    Snackbar.make(drawer, "Please select or capture an image", Snackbar.LENGTH_SHORT).show();
                }
                else{
                    classificationProgress.setVisibility(View.VISIBLE);
                    classificationResult.setVisibility(View.GONE);

                    final cClassify classifier = new cClassify(context);
                    classifier.setListener(new cClassify.ClassificationCallback() {
                        @Override
                        public void onSuccess(JSONObject response) {
                            classificationProgress.setVisibility(View.GONE);
                            classificationResult.setVisibility(View.VISIBLE);

                            try {
                                String resolvedPredictions = resolvePredictions(response.getJSONArray("predictions"), imageProcessor.getClassIndices());
                                classificationResult.setText(resolvedPredictions);
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }

                        @Override
                        public void onError(String message) {
                            classificationResult.setText(message);
                            classificationProgress.setVisibility(View.GONE);
                            classificationResult.setVisibility(View.VISIBLE);
                        }
                    });

                    classifier.classifyimage(imageProcessor.getImage());
                }
            }
        });
    }

    private String resolvePredictions(JSONArray predictions, JSONObject classIndices) throws JSONException {
        StringBuilder response = new StringBuilder();
        List<Prediction> resolvedPredictions = new ArrayList<>();

        for(int i = 0; i < predictions.getJSONArray(0).length(); i ++){
            Double prediction = predictions.getJSONArray(0).getDouble(i);
            Iterator<String> keys = classIndices.keys();
            while(keys.hasNext()) {
                String key = keys.next();
                int id = classIndices.getInt(key);
                if(id == i){
                    resolvedPredictions.add(new Prediction(prediction, key));
                    break;
                }
            }
        }

        Collections.sort(resolvedPredictions,
                (o1, o2) -> o2.getProbability().compareTo(o1.getProbability()));

        if(resolvedPredictions.get(0).getProbability() < 0.1){
            return "I can't recognize it, are you sure it's a car?";
        }

        for(int i = 0; i < 3; i++){
            Prediction pred = resolvedPredictions.get(i);
            response.append(pred.getLabel()).append(" : ").append(String.format(Locale.ENGLISH, "%.2f", pred.getProbability())).append("\n");
        }
        return response.toString();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        imageProcessor = new ImageProcessor();

        if (requestCode == RESULT_LOAD_IMAGE && resultCode == RESULT_OK && null != data) {
            Uri selectedImage = data.getData();
            String[] filePathColumn = { MediaStore.Images.Media.DATA };

            if(selectedImage == null){
                Snackbar.make(drawer, "Selecting image failed", Snackbar.LENGTH_SHORT).show();
                return;
            }
            Cursor cursor = getContentResolver().query(selectedImage,
                    filePathColumn, null, null, null);
            cursor.moveToFirst();

            int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
            String picturePath = cursor.getString(columnIndex);
            cursor.close();

            imageProcessor.setImageFromUri(this, selectedImage);
            imageView.setImageBitmap(imageProcessor.getImage());

        }
        if (requestCode == CAMERA_REQUEST && resultCode == Activity.RESULT_OK) {
            Bitmap photo = (Bitmap) data.getExtras().get("data");
            Uri tempUri = FileUtils.getImageUri(getApplicationContext(), photo);

            imageProcessor.setImageFromUri(this, tempUri);
            imageView.setImageBitmap(photo);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == CAMERA_PERMISSION_CODE) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "camera permission granted", Toast.LENGTH_LONG).show();
                Intent cameraIntent = new
                        Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
                startActivityForResult(cameraIntent, CAMERA_REQUEST);
            } else {
                Toast.makeText(this, "camera permission denied", Toast.LENGTH_LONG).show();
            }

        }

    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }
        if(id == R.id.action_reconnect){
            checkServerAvailability(this);
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_camera) {
            // Handle the camera action
        } else if (id == R.id.nav_gallery) {

        } else if (id == R.id.nav_slideshow) {

        } else if (id == R.id.nav_manage) {

        } else if (id == R.id.nav_share) {

        } else if (id == R.id.nav_send) {

        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    private void checkServerAvailability(final Context context){
        Logger.d("Checking server availability..");
        serverLoading.setVisibility(View.VISIBLE);
        serverOffline.setVisibility(View.GONE);
        serverOnline.setVisibility(View.GONE);
        cWakeUpServer wakeUpServer = new cWakeUpServer(context);
        wakeUpServer.setListener(new cWakeUpServer.StringCallback() {
            @Override
            public void onSuccess(String response) {
                serverLoading.setVisibility(View.GONE);
                serverOffline.setVisibility(View.GONE);
                serverOnline.setVisibility(View.VISIBLE);

                Logger.i("Server is available, version: " + response);
            }

            @Override
            public void onError(String message) {
                serverLoading.setVisibility(View.GONE);
                serverOnline.setVisibility(View.GONE);
                serverOffline.setVisibility(View.VISIBLE);

                Logger.e("Server is not available");
                Snackbar.make(drawer, "Server is not available", Snackbar.LENGTH_INDEFINITE).setAction("Reconnect", new AvailabilitySnackListener(context)).show();
            }
        });
        wakeUpServer.wakeUp();
    }

    private class AvailabilitySnackListener implements View.OnClickListener{

        private Context context;

        AvailabilitySnackListener(Context context){
            super();
            this.context = context;
        }

        @Override
        public void onClick(View v) {
            checkServerAvailability(this.context);
        }
    }
}
