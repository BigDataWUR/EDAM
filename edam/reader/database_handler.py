import copy
import logging

from edam.reader.base import session

logger = logging.getLogger('edam.reader.logger')
logger.setLevel("DEBUG")


def exists(item):
    try:
        item_dict = copy.deepcopy(item.__dict__)  # type: dict

        item_dict.pop('_sa_instance_state')
        _item = session.query(item.__class__).filter_by(**item_dict).first()
        return _item
    except Exception:
        logger.exception("Exception")
        return None


def add_item(item):
    """
    Stores or updates an item in the database.

    In case insertion is successful
    it returns the item (complemented with the database id). In case it's not
    it will raise an exception.

    Args:
        item: object to be stored in database

    Returns:
        The item stored in the database (along with the ID)
    """
    try:
        existing_object = exists(item)
        if existing_object is None:
            session.add(item)
            session.commit()
            # session.flush()
            logger.debug(f"Added {item} in db")
            return item
    except BaseException:
        logger.error(
            f'Exception when adding {item}. Check __add_item__()')
        session.rollback()
        raise
    else:
        return existing_object


def get_all(item):
    session.flush()
    return session.query(item).all()


def add_items(items: list):
    """
    Adds a list of items in database.

    Calls the `add_item` on multiple items in a list.

    Args:
        items: list with items to be added in database

    Returns:
        The items as added in the database
    """
    unique_items = list(filter(lambda item: exists(item) is None, items))
    if unique_items:
        session.bulk_save_objects(unique_items)
        session.commit()
        session.flush()


def update_object(item):
    session.merge(item)
    session.commit()
    session.flush()
