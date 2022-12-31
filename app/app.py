from mangum import Mangum

from app.main import app

print("For lambda docker set handler.")

handler = Mangum(app)
