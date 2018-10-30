package com.ai.deep.andy.carrecognizer;

import android.annotation.SuppressLint;
import android.graphics.BitmapFactory;
import android.support.annotation.NonNull;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.ai.deep.andy.carrecognizer.GalleryFragment.OnListFragmentInteractionListener;
import com.ai.deep.andy.carrecognizer.dataModel.Image;
import com.orhanobut.logger.Logger;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.List;

public class GalleryRecyclerViewAdapter extends RecyclerView.Adapter<GalleryRecyclerViewAdapter.ViewHolder> {

    private final List<Image> mValues;
    private final OnListFragmentInteractionListener mListener;

    @SuppressLint("SimpleDateFormat")
    private SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-mm-dd hh:mm");

    GalleryRecyclerViewAdapter(List<Image> items, OnListFragmentInteractionListener listener) {
        Logger.i("Initializing recycle view with " + items.size() + " image");
        mValues = items;
        mListener = listener;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.fragment_gallery, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull final ViewHolder holder, int position) {
        holder.mItem = mValues.get(position);
        if(holder.mItem.getBitmap() == null) {
            Logger.d("Getting file from directory: " + holder.mItem.getPath());
            File imgFile = new File(holder.mItem.getPath());
            if (imgFile.exists()) {
                holder.mItem.setBitmap(BitmapFactory.decodeFile(imgFile.getAbsolutePath()));
                holder.imageView.setImageBitmap(holder.mItem.getBitmap());
            }
        }
        else {
            holder.imageView.setImageBitmap(holder.mItem.getBitmap());
        }
        holder.predictionsView.setText(mValues.get(position).getMainPrediction());
        holder.classificationDateView.setText(simpleDateFormat.format(mValues.get(position).getLastClassificationDate()));

        holder.mView.setOnClickListener(v -> {
            if (null != mListener) {
               mListener.onListFragmentInteraction(holder.mItem);
            }
        });
    }

    @Override
    public int getItemCount() {
        return mValues.size();
    }

    class ViewHolder extends RecyclerView.ViewHolder {
        final View mView;
        final ImageView imageView;
        final TextView predictionsView;
        final TextView classificationDateView;
        Image mItem;

        ViewHolder(View view) {
            super(view);
            mView = view;
            imageView = view.findViewById(R.id.gallery_img);
            predictionsView = (TextView) view.findViewById(R.id.predictions);
            classificationDateView = (TextView) view.findViewById(R.id.classification_date);
        }
    }
}
