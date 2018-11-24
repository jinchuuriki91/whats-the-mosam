import _thread


def run_in_thread(func):
    def function_wrapper(*args):
        _thread.start_new_thread(func, (*args,))
    return function_wrapper