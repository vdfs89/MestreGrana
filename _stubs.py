class _Sidebar:
    def markdown(self, *a, **k):
        return None
    def header(self, *a, **k):
        return None

class _St:
    sidebar = _Sidebar()

    def markdown(self, *a, **k):
        return None

    def set_page_config(self, *a, **k):
        return None

    def error(self, *a, **k):
        return None

    def warning(self, *a, **k):
        return None

    def info(self, *a, **k):
        return None

    def stop(self, *a, **k):
        raise SystemExit()

    def title(self, *a, **k):
        return None

    def columns(self, n):
        class Col:
            def metric(self, *a, **k):
                return None
        return [Col() for _ in range(n)]

    def markdown(self, *a, **k):
        return None

    def cache_resource(self, *a, **k):
        if a and callable(a[0]):
            return a[0]
        def deco(f):
            return f
        return deco

    def cache_data(self, *a, **k):
        if a and callable(a[0]):
            return a[0]
        def deco(f):
            return f
        return deco

st = _St()
