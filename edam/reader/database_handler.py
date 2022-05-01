import copy
import logging

from edam.reader.base import db_session

logger = logging.getLogger('edam.reader.logger')


def exists(item):
    session = db_session
    try:
        item_dict = copy.deepcopy(item.__dict__)  # type: dict

        item_dict.pop('_sa_instance_state')
        item_exists = session.query(item.__class__).filter_by(**item_dict)
        if item_exists.count() > 0:
            session.flush()
            session.expunge_all()
            session.close()
            return item_exists.first()
        return None
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
    session = db_session
    try:
        item_dict = copy.deepcopy(item.__dict__)  # type: dict

        item_dict.pop('_sa_instance_state')
        item_exists = session.query(item.__class__).filter_by(**item_dict)
        if item_exists.count() > 0:
            session.flush()
            session.expunge_all()
            session.close()
            return item_exists.first()
        else:
            session.add(item)
            logger.debug(f"Added {item} in db")
            session.commit()
    except BaseException:
        logger.error(
            f'Exception when adding {item}. Check __add_item__()')
        session.rollback()
        raise
    session.expunge_all()
    session.close()
    return item


def get_all(item):
    session = db_session
    session.flush()

    return session.query(item).all()


def add_items(items: list) -> list:
    """
    Adds a list of items in database.

    Calls the `add_item` on multiple items in a list.

    Args:
        items: list with items to be added in database

    Returns:
        The items as added in the database
    """

    return list(map(add_item, items))


def update_object(item):
    session = db_session

    session.merge(item)
    session.flush()
    session.expunge_all()
    session.commit()
    session.close()
