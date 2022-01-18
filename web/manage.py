from flask.cli import FlaskGroup

from project import app, db
from project.models import User, Track, Channel


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(Channel(id=1, tags="traumprinz, lost house, planet uterus, dj metatron, dj healer, endless chill, working environment, prime minister of doom, essential giegling, home/club listening", color="blue", link="http://lon1.apankov.net:8090/traumprinz"))
    db.session.add(Channel(id=2, tags="yurets collection, random selection, best of, literally anything, musical encyclopedia, nobrow mashup, deep (re)search, egalitarism, librarian punk, experiments on freedom, jingles and jungles, answer from above, time waste, cryptoacoustic, sonic artefacts, great archive of human civilization, slice of eternity, blood and milk", color="red", link="http://lon1.apankov.net:8090/yurets"))
    db.session.commit()


if __name__ == "__main__":
    cli()
