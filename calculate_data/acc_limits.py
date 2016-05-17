def get_limits(accel_max, n_samples, window_len):

    window = window_len/2
    MIN = accel_max-window
    MAX = accel_max+(window-1)

    if MIN < 0:
        MIN = 0

    if MAX > n_samples-1:
        MAX = n_samples -1

    return int(MIN), int(MAX)