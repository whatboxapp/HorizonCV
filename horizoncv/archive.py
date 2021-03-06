

#======================================
# demo.py

# class Model():
#     """ Formalize the [pitch, roll] combination. """
#     def __init__(self):
#         self.pitch = None
#         self.roll = None

#     def sendMessage(self):
#         print('REPORT pitch={0:.2f} roll={1:.2f}'.format(self.pitch, self.roll))

# def basic_test():
#     img = load_img('../img/taxi_rotate.png') #'../img/runway1.JPG' taxi_empty.jpg ocean sunset grass
#     good_line = score_line(img, m=0.0, b=20)
#     bad_line = score_line(img, m=2.0, b=0)
#     assert good_line > bad_line
#     print('Basic test of scoring...')

# def time_score():
#     import timeit
#     result = timeit.timeit('horizon.score_line(img, m=0.0,  b=20)', 
#                         setup='import horizon; img=horizon.load_img();', 
#                         number=1000)
#     print('Timing:', result/1000, 'seconds to score a single line.')

#======================================
# horizon.py

# def convert_pitch_roll_to_m_b(pitch, bank):
#     """ 
#         Limits of (pitch, roll) space are [-pi/2, pi/2] for pitch and [0%, 100%] for roll
#     """
#     m = math.tan(bank) #TODO
#     b = None
#     return (m, b)


# TODO more efficient implementation
# def img_line_mask2(rows, columns, m, b):
#     """ Params:
#             rows (int)
#             columns (int)
#             m (double)
#             b (double)
#         Returns:
#             rows x columns np.array boolean mask with True for all values above the line
#     """
#     mask = np.zeros((rows, columns), dtype=np.bool)
#     for x in range(columns):
#         y = m * x + b
#         # ind = np.arange(0, min(int(y), int(rows)))
#         ind = np.arange(max(0, int(y)), int(rows))
#         # print(y, ind)
#         mask[ind, x] = True
#     return mask


# def print_results(m, b, m2, b2):
#     print('\tInitial answer - m:', m, '  b:', b)
#     print('\tAccelerate search...')
#     print('\tRefined_answer: - m:', m2, '  b:', b2)

# scores = list(map(lambda x: score_line(img, x[0], x[1]), grid))
# assert len(scores) > 0, 'Invalid slope and intercept ranges: ' + str(slope_range) + str(intercept_range)
# max_index = np.argmax(scores)
# m, b = grid[max_index]


def convert_m_b_to_pitch_bank(m, b, sigma_below):
    """ 'The pitch angle cannot be exactly calculated from an arbitrary horizon line, however
            the pitch angle will be closely proportional to the percentage of the image above 
            or below the line.'
        Pitch angle (Theta) = size(ground) / size(ground) + size(sky)
        Bank angle (Phi) = tan^-1(m)
    """

    bank = math.degrees(math.atan(m))
    
    # method from original paper
    pitch = sigma_below

    # method from 
    # 'Road environment modeling using robust perspective analysis and recursive Bayesian segmentation'
    # focal_x = 64.4 #
    # focal_y = 37.2 #
    # s = 0
    # x0 = 25 / 2 # image center, in pix
    # y0 = 52 / 2 # image center, in pix
    # cam_calibration = np.array([[focal_x, s, x0], 
    #                             [0, focal_y, y0],
    #                             [0, 0, 1]])
    # v = np.array([x0, b, 1])
    # v_prime = np.linalg.solve(cam_calibration, v)
    # print(v_prime, b)
    # pitch = math.atan(v[1])

    # method from http://eprints.qut.edu.au/12839/1/3067a485.pdf
    # u = 5
    # v = m * u + b
    # f = 35.0
    # inner = (u * math.sin(bank) + v * math.sin(bank)) / f
    # # print(math.atan(inner), math.atan(- inner), math.atan(inner) - math.atan(- inner))
    # pitch = math.atan(inner)
    # print(inner, pitch)

    # method from https://www.researchgate.net/publication/
    #   220143231_Sub-sampling_Real-time_vision_for_micro_air_vehicles
    # images are 29 x 35, or 36 x 64
    # h = 29 # height of image
    # w = 35.0
    # h = 20
    # w = 35
    # y = m * (w / 2.0) + b # y-coordinate of line at half of the screen
    # FOVv = 40 # camera's vertical field of view
    # pitch = y * FOVv / h

    return pitch, bank