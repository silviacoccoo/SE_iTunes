from dataclasses import dataclass

@dataclass
class Album:
    id_album: int
    nome_album: str
    durata_album: float

    def __str__(self):
        return self.nome_album

    def __repr__(self):
        return self.nome_album

    def __hash__(self):
        return hash(self.id_album)