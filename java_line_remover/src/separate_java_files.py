import os
import os.path
from shutil import copyfile


def main():
    size = len([name for name in os.listdir('../java_files')])
    # print('The folder has {} Java files, how much % would you like to transfer to test directory?'.format(size))
    # test_size = int(int(input()) * 0.01 * size)
    # print('And how much % to the validation directory')
    # validation_size = int(int(input()) * 0.01 * size)
    test_size = 0.10 * size
    validation_size = 0.10 * size
    src_path = '../dataset/'
    os.makedirs('../dataset/test', exist_ok=True)
    os.makedirs('../dataset/validation', exist_ok=True)
    os.makedirs('../dataset/train', exist_ok=True)
    directory = os.fsencode('../java_files')
    count = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if count < test_size:
            copyfile('../java_files/' + str(filename), src_path + 'test/' + str(filename))
        elif count < test_size + validation_size:
            copyfile('../java_files/' + str(filename), src_path + 'validation/' + str(filename))
        else:
            copyfile('../java_files/' + str(filename), src_path + 'train/' + str(filename))
        count += 1


main()
