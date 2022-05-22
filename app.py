from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

conn = sqlite3.connect('report.db')
curs = conn.cursor()


app = FastAPI()
origins = [    
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root(group_id: int = 0, start: int = 0, end: int = 0):
    global curs
    curs.execute(f''' SELECT * FROM `groups` 
        WHERE date_start >= {start} AND
        date_end <= {end} AND
        id_bitrix = {group_id}
        ''')

    groups = curs.fetchall()
    current_groups = []
    for item in groups:
        current_groups.append({
            'name': item[0],
            'group_id': item[1],
            'time_s': item[2],
            'date_start': item[3],
            'date_end': item[4],
        })

    return {'groups': current_groups, 'start': start, 'end': end}

