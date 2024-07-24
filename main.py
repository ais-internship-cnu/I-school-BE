from fastapi import FastAPI, Query, Body, HTTPException
#from model import *
#from db import session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],     
    allow_headers=["*"],     
)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



@app.post('/api/v1/course-timetables')
async def postCourseToTimetable(userId : int = Body(...,embed=True),
               timetableId : int = Body(...,embed=True),
               courseId : int = Body(...,embed=True)):
    
    timetable = CourseTimetable()
    timetable.timetable_id = timetableId
    timetable.course_id = courseId 




    timetable = session.query(Timetable).filter(Timetable.timetable_id == timetableId).first()
    print(f'{timetable}')
    if not timetable:
        return {
            "success" : False,
            "data" : "Invalid timetable_id",
            "error" : None    
            }

    # courseId가 course 테이블에 존재하는지 확인
    course = session.query(Course).filter(Course.course_id == courseId).first()
    if not course:
        return {
            "success" : False,
            "data" : "Invalid course_id",
            "error" : None    
            }


    try :
        session.add(timetable)
        session.commit()
        return {
            "success" : True,
            "data" : None,
            "error" : None    
            }

    except SQLAlchemyError as e:
        return {
            "success" : False,
            "data" : None,
            "error" : e    
            }

