# 속 알맹인 Crud

from models import Timetable, CourseTimetable, Course, CourseReview
from domain.course_review import course_review_schema
from sqlalchemy.orm import Session

from utils import UvicornException
from models import CourseReview

# /api/v1/course-reviews/?course-name={course_name}&professor={professor}

def read_course_reviews(course_name: str, professor: str, db: Session):
    # 1. course_name, prof 를 통해 course를 찾는다
    courses = db.query(Course).filter((Course.name == course_name) & (Course.professor == professor)).all()
    if not courses:
        raise UvicornException(status_code=400, message="강의가 존재하지 않습니다.")

    # [<object 'Course'>, ...]
    total_course_reviews = []
    for course in courses:
        course_reviews = db.query(CourseReview).filter(CourseReview.course_id == course.id).all()
        total_course_reviews += course_reviews

    data = course_review_schema.CourseReviews(
        courseName=courses[0].name,
        courseReviews=[course_review_schema.CourseReview(
            rating=course_review.rating,
            content=course_review.content
        ) for course_review in total_course_reviews]
    )
    return data


    # combined_reviews = [review for course in filtered_courses for review in course['reviews']]
    # response = {
    #     "success": True,
    #     "data": {
    #         "courseName": courseName,
    #         "professor": professor,
    #         "courseReviews": combined_reviews
    #     },
    #     "error": None
    # }
    # return response