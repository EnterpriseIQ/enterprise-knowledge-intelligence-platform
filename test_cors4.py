from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

client = TestClient(app)
response = client.options("/", headers={"Origin": "https://attacker.com", "Access-Control-Request-Method": "GET"})
print("OPTIONS Status Code:", response.status_code)
print("OPTIONS Headers:", response.headers)

response2 = client.get("/", headers={"Origin": "https://attacker.com"})
print("GET Status Code:", response2.status_code)
print("GET Headers:", response2.headers)
