# add title and subtitle on api
def decorator_api_titles(**options):
    title = options.get("title", "")
    subtitle = options.get("subtitle", "")

    def dec_method(method):
        def add_logic(request, *args, **kwargs):
            response = method(request, *args, **kwargs)

            response.data["title"] = title
            response.data["subtitle"] = subtitle
            return response

        return add_logic

    return dec_method
