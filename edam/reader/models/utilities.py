from edam.reader.database_handler import update_object, exists


def update_existing(obj, new_values, logger):
    for key, value in new_values.items():
        try:
            if key in ['tags', 'qualifiers']:
                temp = getattr(obj, key)  # type: dict
                try:
                    value.update(temp)
                except ValueError as exception:
                    logger.warning(f"{exception}")
            setattr(obj, key, value)
        except AttributeError:
            logger.warning(f"{key} does not exist")
    if exists(obj) is None:
        update_object(obj)
