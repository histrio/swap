from google.appengine.ext import ndb


class Item(ndb.Model):
    """Models an Item to swap entry with desciption only."""
    description = ndb.StringProperty()
    owner_id = ndb.StringProperty()

    @classmethod
    def get_by_owner(cls, owner_id):
        result = cls.query().filter(cls.owner_id == owner_id).fetch()
        return [item.details() for item in result]

    def details(self):
        result = self.to_dict(exclude=['owner_id'])
        result.update({'id': self.key.id()})
        return result

    @classmethod
    def owned_by(cls, item_id, owner_id):
        item = ndb.Key(cls, item_id).get()
        return item.owner_id == owner_id

    @classmethod
    def exists(cls, item_id):
        item = ndb.Key(cls, item_id).get()
        return (item is not None)

    @classmethod
    @ndb.transactional(xg=True)
    def swap(cls, my_item_id, other_item_id):
        my = ndb.Key(cls, my_item_id).get()
        other = ndb.Key(cls, other_item_id).get()
        my.owner_id, other.owner_id = other.owner_id, my.owner_id
        ndb.put_multi([my, other])
