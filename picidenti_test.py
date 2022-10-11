import cv2
import pyscreenshot as ImageGrab
import numpy as np
import autopy
import time

# autopy.key.tap('a')

screen_size = 0
screen_start_point = 0
screen_end_point = 0


def check_screen_size():
    img = ImageGrab.grab()
    global screen_size
    global screen_start_point
    global screen_end_point

    screen_size = (img.size[0], img.size[1])
    screen_start_point = (screen_size[0] * 0.25, screen_size[1] * 0.15)
    screen_end_point = (screen_size[0] * 0.65, screen_size[1] * 0.65)
    print("Screen size is " + str(screen_size))
    print(screen_start_point)
    print(screen_end_point)


def make_screenshot():
    print(screen_start_point)
    check_screen_size()
    img = ImageGrab.grab(bbox=(int(screen_start_point[0]), int(screen_start_point[1]),
                               int(screen_end_point[0]), int(screen_end_point[1])))
    # img.show()
    img.save('p1.png')


def analysis(template_img='p_templator.png', src_img='p1.png', success_img='success.png'):
    template = cv2.imread(template_img, 0)
    img_rgb = cv2.imread(src_img)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # print('got images')
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    print(res)
    threshold = 0.8
    loc = np.where(res >= threshold)
    print(loc)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)
    if loc[0].any():
        print('Found pic')
        cv2.imwrite(success_img, img_rgb)
        # center = (loc[1][0] + w / 2) / 2, (loc[0][0] + h / 2) / 2
        center = (loc[1][0] + w / 2), (loc[0][0] + h / 2)
        print(center)
        return center
    else:
        print('not found')
        return None


def monitor_mouse_location():
    while True:
        print(autopy.mouse.location())
        time.sleep(1)


def move_mouse(place):
    x, y = place[0], place[1]
    print("Moving cursor to " + str(place))
    autopy.mouse.smooth_move(screen_start_point[0] + x, screen_start_point[1] + y)


def run():
    make_screenshot()
    x, y = analysis()
    move_mouse((x, y))


run()
