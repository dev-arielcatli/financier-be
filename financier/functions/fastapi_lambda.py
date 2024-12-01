from fastapi import FastAPI

from mangum import Mangum

app = FastAPI()

@app.get('/api')
async def main():
    return {
        "statusCode": 200,
        "body": "Hello, world"
    }


handler = Mangum(app)