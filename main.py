from fastapi import Request, FastAPI, HTTPException
from solve_captcha import solve_base64

app = FastAPI()


@app.get('/')
async def read_root(request: Request):
    return 'OK'


@app.post('/solve')
async def read_root(request: Request):
    if(request.headers['authorization'] != 'Bearer s6Y!zLDz18bFUSYm9O7%5$ZDu%E4BhFrArGptTBW8XSOx2G2GcOqk*&YLxkgY8rnILBj0&!4oc9mrojs%vhFDIHg7z!xQz%B&JgsUi5DUpSuZSxh7VY#0H54nTO6yDBC'):
        raise HTTPException(status_code=401, detail='Unauthorized')
    body = await request.body()
    solution = solve_base64(body)
    return solution
