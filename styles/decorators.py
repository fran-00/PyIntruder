def white_text(func):
    def wrapper(*args, **kwargs):
        string = func(*args, **kwargs)
        return f"<span style='color: #FFFFFF;'>{string}</span>"
    return wrapper

def red_text(func):
    def wrapper(*args, **kwargs):
        string = func(*args, **kwargs)
        return f"<span style='color: #FF0000;'>{string}</span>"
    return wrapper

def green_text(func):
    def wrapper(*args, **kwargs):
        string = func(*args, **kwargs)
        return f"<span style='color: #00FF00;'>{string}</span>"
    return wrapper

def blue_text(func):
    def wrapper(*args, **kwargs):
        string = func(*args, **kwargs)
        return f"<span style='color: #0000FF;'>{string}</span>"
    return wrapper

def underline_text(func):
    def wrapper(*args, **kwargs):
        string = func(*args, **kwargs)
        return f"<span style='text-decoration: underline;'>{string}</span>"
    return wrapper

def bold_text(func):
    def wrapper(*args, **kwargs):
        string = func(*args, **kwargs)
        return f"<span style='font-weight: bold;'>{string}</span>"
    return wrapper
