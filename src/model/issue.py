
class Issue(object):

    def __init__(self, name, id, releasedate, released: bool = False):
        self.name = name
        self.id = id
        self.releasedate = releasedate
        self.released: bool = released

    def set_editor(self, editor):
        # TODO: Implement me!
        pass

