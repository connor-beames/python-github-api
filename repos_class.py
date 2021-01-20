
class Repo:
    """attempt to model a repo"""

    def __init__(self, name, owner, stars, repository, description):
        """initializes a repo"""
        self.name = name
        self.owner = owner
        self.stars = stars
        self.repository = repository
        self.description = description