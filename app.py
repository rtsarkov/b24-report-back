from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

conn = sqlite3.connect('report.db')
curs = conn.cursor()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def group(group_id: int = 0, start: int = 0, end: int = 0):
    global curs
    curs.execute(f''' SELECT p_t.time_s as time, g.bitrix_id as bitrix_id 
        FROM `plan_time` as p_t 
        LEFT JOIN `groups` as g ON p_t.group_id = g.id
        WHERE p_t.date_start >= {start} AND
        p_t.date_end <= {end} AND
        g.bitrix_id = {group_id}
        ''')

    groups = curs.fetchall()
    current_groups = []
    for item in groups:
        current_groups.append({
            'time': item[0],
            'group_id': item[1],
        })

    return {'groups': current_groups}

@app.get("/groups")
async def groups():
    global curs
    groups = curs.execute('SELECT name, bitrix_id, id FROM `groups`').fetchall()
    return groups

@app.post('/groups')
async def groupsAdd(name: str = '', bitrix_id: int = 1):
    global curs, conn    
    curs.execute(f''' INSERT INTO `groups` (name, bitrix_id)
                VALUES ("{name}", {bitrix_id}) ''')
    conn.commit()
    return curs.lastrowid

@app.delete('/groups')
async def groupsDelete(id: int):
    global curs, conn    
    curs.execute(f''' DELETE FROM `groups` WHERE id={id} ''')
    conn.commit()
    return id


@app.get('/time')
async def times():
    global curs
    times = curs.execute(''' 
        SELECT p_t.id as time_id, p_t.time_s, p_t.date_start, p_t.date_end, g.name, g.bitrix_id FROM `plan_time` as p_t
        LEFT JOIN `groups` as g ON p_t.group_id = g.id ORDER BY `time_id` DESC
    ''').fetchall()
    current_times = []
    for item in times:
        current_times.append({
            'time_id': item[0],
            'time': item[1],
            'date_start': item[2],
            'date_end': item[3],
            'group_name': item[4],
            'bitrix_id': item[5],
        })
    return current_times

@app.post('/time')
async def timeAdd(group_id: int, time_s: int, date_start: int, date_end: int):
    global curs, conn  
    curs.execute(f''' INSERT INTO `plan_time` (group_id, time_s, date_start, date_end)
                VALUES ({group_id}, {time_s}, {date_start}, {date_end}) ''')
    conn.commit()
    return curs.lastrowid

@app.delete('/time')
async def timesDelete(id: int):
    global curs
    curs.execute(f''' DELETE FROM `plan_time` WHERE id={id} ''')
    conn.commit()
    return id
