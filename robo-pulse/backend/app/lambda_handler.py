'''
Day 9 - Entry point that AWS Lambda actually calls. Magnum
translates between Lambda's event context invocation model
and the ASGI interface that FastAPI already speaks.
app.main:app itself will need zero changes to run inside
Lambda. 
'''

from mangum import Mangum

from app.main import app

handler = Mangum(app)