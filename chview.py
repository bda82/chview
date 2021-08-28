from aiohttp import web
import os
from aiohttp import web
import aiohttp_jinja2
from infi.clickhouse_orm.fields import UInt16Field
import jinja2

from infi.clickhouse_orm import Database, Model, MergeTree, Memory

from infi.clickhouse_orm import (
    MergeTree,
    UUIDField,
    DateTimeField,
    Float32Field,
    Int32Field,
    StringField
)


CH_HOST = 'desire.r-admin.ru'
CH_PORT = 8123
CH_USER = 'root'
CH_PASSORD = 'password'
CH_DB = 'clickhouse'
CH_TABLE = 'desire_logs'


class BaseModel(Model):
    db = Database(db_name=CH_DB,
                  db_url=f'http://{CH_HOST}:{CH_PORT}/',
                  username=CH_USER,
                  password=CH_PASSORD)


class Desire_Logs(BaseModel):
    name = StringField()
    source_uuid = StringField()
    msg = StringField()
    levelname = StringField()
    pathname = StringField()
    filename = StringField()
    module = StringField()
    lineno = UInt16Field()
    funcName = StringField()
    dt = DateTimeField()

    engine = MergeTree(partition_key=['toYYYYMM(ts)'], order_by=('dt', 'name'))

    @property
    def json(self):
        return dict(
            name=self.name,
            source_uuid=self.source_uuid,
            msg=self.msg,
            levelname=self.levelname,
            pathname=self.pathname,
            filename=self.filename,
            module=self.module,
            lineno=self.lineno,
            funcName=self.funcName,
            dt=self.dt,
        )


def query_select(limit=10, offset=0):
    return f'SELECT * FROM {CH_TABLE} LIMIT {limit} OFFSET {offset}'


def get_logs(limit=10):
    rv = Desire_Logs.objects_in(Desire_Logs.db).filter().order_by('-dt')
    res = list(map(lambda x: x.json, rv))
    return res



@aiohttp_jinja2.template('index.jinja2')
async def index(request):
    rv = get_logs()
    return {'data': rv}


app = web.Application()
app.add_routes([web.get('/', index)])

aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), 
                                                    "templates")))

web.run_app(app)