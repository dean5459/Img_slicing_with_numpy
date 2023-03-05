import requests
from io import BytesIO
from PIL import Image, ImageFilter
import numpy as np
import csv


def numpy_operations_on_img_arr(img_array):
    mean = np.mean(img_array)
    sum = np.sum(img_array)
    std = np.std(img_array)
    with open('image_statistics.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Statistic", "Value"])
        writer.writerow(["Mean", mean])
        writer.writerow(["Sum", sum])
        writer.writerow(["Standard Deviation", std])


def image_filter(img_array):
    filtered_array = np.array(Image.fromarray(img_array).filter(ImageFilter.GaussianBlur(radius=5)))
    filtered_image = Image.fromarray(filtered_array)

    return filtered_image


def slice_vertical(img_array):
    slices = np.split(img_array, 50, axis=1)

    image1_slices = slices[1::2]
    image1_array = np.concatenate(image1_slices, axis=1)

    image2_slices = np.delete(slices, np.s_[1::2], axis=0)
    image2_array = np.concatenate(image2_slices, axis=1)

    combined_array = np.concatenate((image1_array, image2_array), axis=1)

    return combined_array


def slice_horizontal(img_array):
    slices = np.split(img_array, 50, axis=0)

    image3_slices = slices[1::2]
    image3_array = np.concatenate(image3_slices, axis=0)

    image4_slices = np.delete(slices, np.s_[1::2], axis=0)
    image4_array = np.concatenate(image4_slices, axis=0)

    combined_array = np.concatenate((image3_array, image4_array), axis=1)
    combined_image = Image.fromarray(combined_array)

    return combined_image


if __name__ == '__main__':

    url = "https://imgs.search.brave.com/CPOTItPl75HWnEu2r-GwOKLTVsRqX7_2Dk9LN_hnHu4/rs:fit:1200:1200:1/g:ce/aHR0cHM6Ly93YWxs/cGFwZXJjYXZlLmNv/bS93cC9tTHpuUWQ1/LmpwZw"
    response = requests.get(url)

    img = Image.open(BytesIO(response.content))
    img_array = np.array(img)

    #numpy mathematical operations
    numpy_operations_on_img_arr(img_array)

    #image filtering
    filtered_image = image_filter(img_array)
    filtered_image.save('filtered_wolf.jpg')

    #'we live in the matrix' thing
    vertically_sliced_image_array = slice_vertical(img_array)
    horizontally_sliced_image = slice_horizontal(vertically_sliced_image_array)
    horizontally_sliced_image.save("wolf_breeder.jpg")