# in grid/__init__.py
import os
from py4web import action, Field, DAL
from py4web.utils.grid import Grid, GridClassStyleBulma
from py4web.utils.form import Form, FormStyleBulma
from yatl.helpers import A


# database definition
DB_FOLDER = os.path.join(os.path.dirname(__file__), 'databases')
if not os.path.isdir(DB_FOLDER):
   os.mkdir(DB_FOLDER)
db = DAL('sqlite://storage.sqlite', folder=DB_FOLDER)
db.define_table(
   'person',
   Field('superhero'),
   Field('name'),
   Field('job'),
	Field.Virtual('description', lambda row: f"{row.name} ({row.job}) aka {row.superhero}"),
   )

# add example entries in db
if not db(db.person).count():
   db.person.insert(superhero='Superman', name='Clark Kent', job='Journalist')
   db.person.insert(superhero='Spiderman', name='Peter Park', job='Photographer')
   db.person.insert(superhero='Batman', name='Bruce Wayne', job='CEO')
   db.commit()

@action('index', method=['POST', 'GET'])
@action('index/<path:path>', method=['POST', 'GET'])
@action.uses('grid.html', db)
def index(path=None):
   grid = Grid(path,
            formstyle=FormStyleBulma, # FormStyleDefault or FormStyleBulma
            grid_class_style=GridClassStyleBulma, # GridClassStyle or GridClassStyleBulma
            query=(db.person.id > 0),
            orderby=[db.person.name],
            search_queries=[['Search by Name', lambda val: db.person.name.contains(val)]])

   return dict(grid=grid)