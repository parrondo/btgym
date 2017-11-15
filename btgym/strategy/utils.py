import  numpy as np


def log_transform(x):
    return np.sign(x) * np.log(np.fabs(x) + 1)


def tanh(x):
    return 2 / (1 + np.exp(-2 * x)) - 1


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def abs_norm_ratio(x, a, b):
    """
    Norm. V-shaped realtive position of x in [a,b], a<=x<=b.
    """
    return abs((2 * x - a - b) / (abs(a) + abs(b)))


def norm_log_value(current_value, start_value, drawdown_call, target_call, epsilon=1e-4):
    """
    Current value log-normalized in [-1,1] wrt p/l limits.
    """
    x = np.asarray(current_value)
    x = (x / start_value - 1) * 100
    x = (x - target_call) / (drawdown_call + target_call) + 1
    x = np.clip(x, epsilon, 1 - epsilon)
    x = 1 - 2 * np.log(x) / np.log(epsilon)
    return x


def norm_value(current_value, start_value, drawdown_call, target_call, epsilon=1e-8):
    """
    Current value normalized in [-1,1] wrt upper and lower bounds
    """
    x = np.asarray(current_value)
    x = (x / start_value - 1) * 100
    x = (x - target_call) / (drawdown_call + target_call) + 1
    x = 2 * np.clip(x, epsilon, 1 - epsilon) - 1
    return x


def decayed_result(trade_result, current_value, start_value, drawdown_call, target_call, gamma=1.0):
    """
    Normalized in [-1,1] trade result, lineary decayed wrt current_value.
    """
    target_value = start_value * (1 + target_call / 100)
    value_range = start_value * (drawdown_call + target_call) / 100
    decay = (gamma - 1) * (current_value - target_value) / value_range + gamma
    x = trade_result * decay / value_range
    return x


def exp_scale(x, gamma=4):
    """
    Returns exp. scaled value in [0.01,1] for x in [0,1]; gamma controls steepness.
    """
    x = np.asarray(x) + 1
    return np.clip(np.exp(x ** gamma - 2 ** gamma), 0.01, 1)