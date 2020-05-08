import os

def check_all_image_id_uniqueness():
    pass

"""
it's created to solve 1 inconsistency ..
i did not delete it, but don't use this again!!
"""
def id_fix_v1():
    start_id = 27088
    file_path = 'D:\\Projects\\CarRecognizer\\data2\\autoscout\\meta\\BMW'
    image_path = "D:\\Projects\\CarRecognizer\\data2\\autoscout\\images\\BMW\\"
    forbidden_dirs = ['732', 'Z8', 'X5', '633', '315', '745', 'Z4,']

    for file_dir in os.listdir(file_path):
        if file_dir not in forbidden_dirs:
            car_dir = file_path + '\\' + file_dir
            for file_name in os.listdir(car_dir):
                make, model, id = file_name[:-4].split('_')
                new_file_name = make + '_' + model + '_' + str(int(id) + start_id) + '.txt'
                os.rename(car_dir + '\\' + file_name, car_dir + '\\' + new_file_name)
                print('rename done new id %s' % new_file_name)
                print('syncing images to car new id..')
                car_img_path = image_path + model
                for image_name in os.listdir(car_img_path):
                    m, mm, car_id, image_id = image_name[:-4].split('_')
                    if int(id) == int(car_id):
                        old_image_name = car_img_path + '\\' + image_name
                        new_image_name = car_img_path + '\\' + make + '_' + model + '_' + str(int(id) + start_id) + '_' + image_id + '.jpg'
                        os.rename(old_image_name, new_image_name)
                        print('File renamed from %s to %s' % (old_image_name, new_image_name))


id_fix_v1()