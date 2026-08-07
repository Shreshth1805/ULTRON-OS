_MODELS = {}


def register_model(
    name,
    model
):

    _MODELS[name] = model


def get_model(
    name
):

    return _MODELS.get(name)


def list_models():

    return list(_MODELS.keys())