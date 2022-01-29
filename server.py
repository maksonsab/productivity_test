from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
def main():
    return 'Hello world!' 




if __name__ == '__main__':
    uvicorn.run("server:app", port=8000, host='0.0.0.0', reload = True)