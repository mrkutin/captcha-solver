from fastapi import Request, FastAPI, HTTPException
import uvicorn
from solve_captcha import solve_base64
import os

app = FastAPI()


@app.get('/')
async def read_root():
    return 'OK'


@app.post('/solve')
async def read_root(request: Request):
    print(f'Bearer {os.environ["TOKEN"]}')
    if(request.headers['authorization'] != f'Bearer {os.environ["TOKEN"]}'):
        raise HTTPException(status_code=401, detail='Unauthorized')
    body = await request.body()
    solution = solve_base64(body)
    return solution

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ['PORT']))