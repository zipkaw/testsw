class UpdateFieldsMixin:
    """
        Update object fields specified in the kwags
    """
    @staticmethod
    def update(object, **kwargs):
        for field, value in kwargs.items():
            object.__setattr__(field, value)
        object.save()
