from dataclasses import dataclass


@dataclass
class Artist:
    artist_id: int
    first_name: str
    last_name: str
    biography: str
    link: str

    def __str__(self):
        return f"Artist(id={self.artist_id}," \
               f"first_name='{self.first_name}', " \
               f"last_name='{self.last_name}', " \
               f"biography='{self.biography}', " \
               f"link='{self.link}')"
