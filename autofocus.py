import io
import cv2  # sudo apt-get install python-opencv
import numpy as np
import os
import time

try:
    import picamera
    from picamera.array import PiRGBArray
except:
    sys.exit(0)


def focusing(val):
    value = (val << 4) & 0x3ff0
    data1 = (value >> 8) & 0x3f
    data2 = value & 0xf0
    # time.sleep(0.5)
    print("focus value: {}".format(val))
    os.system("i2cset -y 0 0x0c %d %d" % (data1, data2))


def sobel(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_sobel = cv2.Sobel(img_gray, cv2.CV_16U, 1, 1)
    return cv2.mean(img_sobel)[0]


def laplacian(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_sobel = cv2.Laplacian(img_gray, cv2.CV_16U)
    return cv2.mean(img_sobel)[0]


def calculation(curr_frame):
    bytes = np.asarray(bytearray(curr_frame), dtype=np.uint8)
    image = cv2.imdecode(bytes, cv2.IMREAD_COLOR)
    return laplacian(image)

def run_autofocus(frame, max_index, max_value, last_value, dec_count, focal_distance):
    print("Start focusing")

    new_max_index = max_index
    new_max_value = max_value
    new_last_value = last_value
    new_dec_count = dec_count
    new_focal_distance = focal_distance

    # Adjust focus
    focusing(new_focal_distance)
    # Take image and calculate image clarity
    val = calculation(frame)
    print(val)
    # Find the maximum image clarity
    if val > new_max_value:
        new_max_index = new_focal_distance
        new_max_value = val

    # If the image clarity starts to decrease
    if val < new_last_value:
        new_dec_count += 1
    else:
        new_dec_count = 0
    # Image clarity is reduced by six consecutive frames
    if new_dec_count > 6:
        focusing(new_max_index)
        print("Camera focused")
        return True

    # Increase the focal distance
    new_focal_distance += 15
    if new_focal_distance > 1000:
        focusing(new_max_index)
        print("Camera focused to infinite")
        return True

    return {
        "max_index": new_max_index,
        "max_value": new_max_value,
        "last_value": new_last_value,
        "dec_count": new_dec_count,
        "focal_distance": new_focal_distance
    }



# if __name__ == "__main__":
#     # open camera
#     camera = picamera.PiCamera()
#
#     # camera.awb_gains=4
#     # camera.exposure_mode='off'
#     # camera.awb_mode='fluorescent'
#     # open camera preview
#     camera.start_preview()
#     # set camera resolution to 640x480(Small resolution for faster speeds.)
#     camera.resolution = (640, 480)
#     time.sleep(0.1)
#     print("Start focusing")
#
#     max_index = 10
#     max_value = 0.0
#     last_value = 0.0
#     dec_count = 0
#     focal_distance = 10
#
#     stream = io.BytesIO()
#
#     for frame in camera.capture_continuous(stream, 'jpeg',
#                                            use_video_port=True):
#
#         # return current frame
#         stream.seek(0)
#         curr_frame = stream.read()
#
#         # Adjust focus
#         focusing(focal_distance)
#         # Take image and calculate image clarity
#         val = calculation(curr_frame)
#         # Find the maximum image clarity
#         print(val)
#         if val > max_value:
#             max_index = focal_distance
#             max_value = val
#
#         # If the image clarity starts to decrease
#         if val < last_value:
#             dec_count += 1
#         else:
#             dec_count = 0
#         # Image clarity is reduced by six consecutive frames
#         if dec_count > 6:
#             break
#         last_value = val
#
#         # Increase the focal distance
#         focal_distance += 15
#         if focal_distance > 1000:
#             break
#
#         stream.seek(0)
#         stream.truncate()
#
#     # Adjust focus to the best
#     focusing(max_index)
#     time.sleep(1)
#     # set camera resolution to 2592x1944
#     camera.resolution = (1920, 1080)
#     # save image to file.
#     camera.capture("test.jpg")
#     print("max index = %d,max value = %lf" % (max_index, max_value))
#     # while True:
#     #	time.sleep(1)
#
#     camera.stop_preview()
#     camera.close()