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
