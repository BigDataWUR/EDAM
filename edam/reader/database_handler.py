import copy
import logging

from edam.reader.base import db_session

database_handler = logging.getLogger('edam.reader.database_handler')


def add_item(item):
    """
    Tries to store an item in the database. In case insertion is successful
    it returns the item (complemented with the database id). In case it's not
    it will raise an exception.
    :param item:
    :return: item
    """
    session = db_session
    session.expire_on_commit = False
    try:
        item_dict = copy.deepcopy(item.__dict__)  # type: dict

        item_dict.pop('_sa_instance_state')
        item_exists = session.query(item.__class__).filter_by(**item_dict)
        if item_exists.count() > 0:
            session.flush()
            session.close()
            return item_exists.first()
        else:
            session.add(item)
            database_handler.debug(f"Added {item} in db")
            session.commit()
    except BaseException:
        database_handler.error(f'Exception when adding {item}. Check __add_item__()')
        session.rollback()
        raise
    finally:
        session.flush()
    session.close()
    return item


def add_items(items):
    """
    Tries to store an item in the database. In case insertion is successful
    it returns the item (complemented with the database id). In case it's not
    it will raise an exception.
    :param items:
    :return: item
    """
    items_to_return = list()

    for item in items:
        items_to_return.append(add_item(item))
    return items_to_return


def update_item(item, metadata_dict):
    session = db_session
    returned_item = session.query(item.__class__).filter(
        item.__class__.id == item.id).first()  # type: item.__class__
    if returned_item:
        returned_item.update_metadata(metadata_dict)
        session.commit()
        database_handler.debug(f"Updated {item}")
        session.close()
