from fastapi import FastAPI, Query, Body, HTTPException
from model import *
from db import session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

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
async def say_hello_name(name: str):
    return {"message": f"Hello {name}"}



@app.post('/api/v1/course-timetables')
async def postCourseToTimetable(userId : int = Body(...,embed=True),
               timetableId : int = Body(...,embed=True),
               code : str = Body(...,embed=True)):
    

    # code로 courseId 찾기
    course = session.query(Course.course_id).filter(Course.code == code).all()
    if not course:
        return {
            "success" : False,
            "data" : "Invalid code",
            "error" : None    
            }


    timetable = session.query(Timetable).filter(Timetable.timetable_id == timetableId).first()
    if not timetable:
        return {
            "success" : False,
            "data" : "Invalid timetable_id",
            "error" : None    
            }
    

    for courseId in course:
        courses = CourseTimetable()
        courses.timetable_id = timetableId
        courses.course_id = courseId[0]

        try :
            session.add(courses)
            session.commit()
            session.refresh(courses)

        except SQLAlchemyError as e:
            return {
                "success" : False,
                "data" : None,
                "error" : e
            }
        
    return{
        "success" : True,
        "data" : None,
        "error" : None  
    }

@app.delete('/api/v1/course-timetables')
async def deleteCourseFromTimetable(userId : int = Body(...,embed=True),
               timetableId : int = Body(...,embed=True),
               code : str = Body(...,embed=True)):
    

    # code로 courseId 찾기
    course = session.query(Course.course_id).filter(Course.code == code).all()
    if not course:
        return {
            "success" : False,
            "data" : "Invalid code",
            "error" : None    
            }


    timetable = session.query(Timetable).filter(Timetable.timetable_id == timetableId).first()
    if not timetable:
        return {
            "success" : False,
            "data" : "Invalid timetable_id",
            "error" : None    
            }
    

    for courseId in course:

        try :
            courseId[0]
            session.query(CourseTimetable).filter(and_(
                CourseTimetable.course_id == courseId[0],
                CourseTimetable.timetable_id == timetableId)).delete()
            session.commit()

        except SQLAlchemyError as e:
            return {
                "success" : False,
                "data" : None,
                "error" : e
            }
        
    return{
        "success" : True,
        "data" : None,
        "error" : None  
    }

