import cv2 as cv


def set_opacity(image, opacity):
    image[:, :, 3] = cv.multiply(image[:, :, 3], opacity)
    return image
    

def rotate_img_uncropped(image, angle):
    # get rotation matrix
    rows, cols = image.shape[:2]
    center = (cols / 2.0, rows / 2.0)
    rot = cv.getRotationMatrix2D(center, angle, 1)
    
    # set max bounds of rotated image
    abs_cos = abs(rot[0, 0]) 
    abs_sin = abs(rot[0, 1])

    bound_cols = int(rows * abs_sin + cols * abs_cos)
    bound_rows = int(rows * abs_cos + cols * abs_sin)

    rot[0,2] += bound_cols / 2.0 - cols / 2.0
    rot[1,2] += bound_rows / 2.0 - rows / 2.0

    # return rotated image
    return cv.warpAffine(image, rot, (bound_cols, bound_rows))


def resize_img_hand_distance(image, landmark_result, base_height, scale=1):
    pass


def add_image_with_alpha(bottom_img, top_img, center_pos, opacity):
    # apply opacity
    if opacity < 1:
        top_img = set_opacity(top_img, opacity)

    # get image shapes and center coordinates
    t_c_x, t_c_y = center_pos
    b_rows, b_cols = bottom_img.shape[:2]
    t_rows, t_cols = top_img.shape[:2]

    # calculate top image coordinates on bottom image
    b_y1 = max(t_c_y - int(t_rows / 2), 0)
    b_y2 = max(min(t_c_y + t_rows - int(t_rows / 2), b_rows), 0)
    b_x1 = max(t_c_x - int(t_cols / 2), 0)
    b_x2 = max(min(t_c_x + t_cols - int(t_cols / 2), b_cols), 0)
    
    # calculate coordinates of bottom images to crop if necessary
    t_y1 = max(t_rows - b_y2, 0)
    t_y2 = max(min(b_rows - b_y1, t_rows), 0)
    t_x1 = max(t_cols - b_x2, 0)
    t_x2 = max(min(b_cols - b_x1, t_cols), 0)

    # calculate alpha value for top and bottom image of area in question
    t_a = top_img[t_y1:t_y2, t_x1:t_x2, 3] / 255.0
    b_a = 1.0 - t_a

    # scale each channel according to alpha and add bottom to top image
    for c in range(3):
        bottom_img[b_y1:b_y2, b_x1:b_x2, c] = bottom_img[b_y1:b_y2, b_x1:b_x2, c] * b_a + \
                                              top_img[t_y1:t_y2, t_x1:t_x2, c] * t_a

    return bottom_img
