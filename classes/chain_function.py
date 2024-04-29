class ChainFunction:
    END = "TERMINATE_FUNCTION_CALL"


    def __init__(self, *methods):
        self.methods = list(methods)

    def __call__(self, *args):
        cur_args = args
        for method in self.methods:
            res = method(*cur_args)
            if res == ChainFunction.END:
                return None

            cur_args = [res]
        
        return res

    def add_at_head(self, method):
        self.methods.insert(0, method)

    def add_at_tail(self, method):
        self.methods.append(method)

    def add_at_index(self, method, i):
        self.methods.insert(i, method)