from fastapi import FastAPI, Query, Body, HTTPException
from models import *
from database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_

app = FastAPI()

origins = [
    "http://localhost:8000"
]

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
    course = SessionLocal.query(Course.course_id).filter(Course.code == code).all()
    if not course:
        return {
            "success" : False,
            "data" : "Invalid code",
            "error" : None    
            }


    timetable = SessionLocal.query(Timetable).filter(Timetable.timetable_id == timetableId).first()
    if not timetable:
        return {
            "success" : False,
            "data" : "Invalid timetable_id",
            "error" : None    
            }
    

    for courseId in course:
        courses = Course_Timetable()
        courses.timetable_id = timetableId
        courses.course_id = courseId[0]

        try :
            SessionLocal.add(courses)
            SessionLocal.commit()
            SessionLocal.refresh(courses)

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
    course = SessionLocal.query(Course.course_id).filter(Course.code == code).all()
    if not course:
        return {
            "success" : False,
            "data" : "Invalid code",
            "error" : None    
            }


    timetable = SessionLocal.query(Timetable).filter(Timetable.timetable_id == timetableId).first()
    if not timetable:
        return {
            "success" : False,
            "data" : "Invalid timetable_id",
            "error" : None    
            }
    

    for courseId in course:

        try :
            courseId[0]
            SessionLocal.query(Course_Timetable).filter(and_(
                Course_Timetable.course_id == courseId[0],
                Course_Timetable.timetable_id == timetableId)).delete()
            SessionLocal.commit()

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


@app.get('/api/v1/courses')
async def getCourses(major: str, keyword: str, grade: str):

    try:
        # 먼저 키워드에 맞는 교수를 확인
        course_check = SessionLocal.query(Course).filter(
            or_(
                Course.professor == keyword,
                Course.name == keyword
            )
        ).all()

        # 키워드에 맞는 교수가 없으면 오류 메시지 반환
        if not course_check:
            return {
                "success": False,
                "data": {
                    "courses": None
                },
                "error": "Not exist prof or Course Name"
            }

        # 키워드가 맞는 경우, major와 grade를 기준으로 필터링
       # Course와 CourseReview 테이블을 join하여 조건에 맞는 데이터를 가져옴
        courses = SessionLocal.query(
            Course.course_id,
            Course.code,
            Course.name,
            Course.professor,
            Course.grade,
            Course.credit,
            Course.day,
            Course.start_time,
            Course.end_time,
            Course.course_room,
            Course_Review.rating.label('review_rating')
        ).join(Course_Review, Course.course_id == Course_Review.course_id, isouter=True).filter(
            and_(
                Course.major == major,
                Course.grade == grade,
                or_(
                    Course.professor == keyword,
                    Course.name == keyword
                )
            )
        ).all()

        print(courses)

        # 데이터를 변환하여 응답 형식에 맞게 변경
        course_list = [
            {
                "courseId": course.course_id,
                "courseCode": course.code,
                "courseName": course.name,
                "professor": course.professor,
                "rating": course.review_rating,
                "grade": course.grade,
                "credit": course.credit,
                "courseDay": course.day,
                "courseStartTime": course.start_time,
                "courseEndTime": course.end_time,
                "courseRoom": course.course_room
            }
            for course in courses
        ]

        return {
            "success": True,
            "data": {
                "courses": course_list
            },
            "error": None
        }
        
    except SQLAlchemyError as e:
        return {
            "success": False,
            "data": None,
            "error": e
        }
    
