from fastapi import Request, FastAPI
from solve_captcha import solve_base64

app = FastAPI()


@app.get('/')
def read_root(request: Request):
    return {'OK'}


@app.post('/solve')
async def read_root(request: Request):
    body = await request.body()
    solution = solve_base64(body)
    return solution
