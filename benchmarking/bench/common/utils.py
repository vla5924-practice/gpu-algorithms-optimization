def print_many(symbol: str, n=40) -> None:
    print(symbol * n)


def print_params(params: dict, space=" ") -> None:
    for key in params:
        print("{}:{}{}".format(key, space, params[key]))
