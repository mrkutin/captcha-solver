from fastapi import Request, FastAPI, HTTPException
from solve_captcha import solve_base64
import os

app = FastAPI()


@app.get('/')
async def read_root(request: Request):
    return 'OK'


@app.post('/solve')
async def read_root(request: Request):
    print(f'Bearer {os.environ["TOKEN"]}')
    if(request.headers['authorization'] != f'Bearer {os.environ["TOKEN"]}'):
        raise HTTPException(status_code=401, detail='Unauthorized')
    body = await request.body()
    solution = solve_base64(body)
    return solution
