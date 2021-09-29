import solver
from all_func import *


path = 'data/data_v1.png'
img = cv2.imread(path)

img_height = 504
img_width = 504
img = cv2.resize(img, (img_width, img_height))

img_show_digit = img.copy()

# find all contours
contours, hierarchy = cv2.findContours(img_handler(img), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# find biggest contours
biggest = np.array([])
biggest = rect_contours(contours)


if biggest.size != 0:
    # find the exact order
    biggest = biggest.reshape((4, 2))
    biggest = four_points(biggest)

    # transform the image
    img_warp = perspective_trans(biggest, img, img_width, img_height)    
    
    boxes = split_img(img_warp) # split in to 81 boxes

    # predict the number in each box
    ques = ques_digit(boxes)

    # check if the value is 0
    pos_arr = np.where(ques > 0, 0, 1)


    # find solution
    board = np.array_split(ques, 9)
    try:
        solver.solve_sud(board)
    except:
        pass
    
    # show the answer
    ans_list = []
    for lst in board:
        for item in lst:
            ans_list.append(item)
    solved_num = ans_list*pos_arr # exist num will be multiplied by 0
    ans_digit = ans_digit(img_show_digit, solved_num)


cv2.imshow('Solution', ans_digit)

sol_path = 'Saved'
if cv2.waitKey(0) & 0xFF == ord('s'):
    cv2.imwrite(os.path.join(sol_path, "solution.jpg"), ans_digit)


##################################################