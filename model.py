from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, BigInteger
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.ext.declarative import declarative_base

from enum import Enum

Base = declarative_base()

# Enum 타입 정의
# class UniversityEnum(str, Enum):
#     SNU = 'Seoul National University'
#     KU = 'Korea University'
#     YU = 'Yonsei University'

# class MajorEnum(str, Enum):
#     CS = 'Computer Science'
#     BA = 'Business Administration'
#     ECO = 'Economics'

# class DayEnum(str, Enum):
#     MON = 'Monday'
#     TUE = 'Tuesday'
#     WED = 'Wednesday'
#     THU = 'Thursday'
#     FRI = 'Friday'
#     SAT = 'Saturday'

# User 테이블 정의
class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=False)
    university = Column(String(255), nullable=False)
    major = Column(String(255), nullable=False)
    entrance_year = Column(BigInteger, nullable=False)
    certification = Column(String(255), nullable=False)
    created_at = Column(Date, default='CURRENT_DATE', nullable=False)

# Timetable 테이블 정의
class Timetable(Base):
    __tablename__ = "timetable"
    timetable_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    name = Column(String(255), nullable=False)

# Course 테이블 정의
class Course(Base):
    __tablename__ = "course"
    course_id = Column(BigInteger, primary_key=True, index=True)
    code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    professor = Column(String(100), nullable=False)
    major = Column(String(255), nullable=False)
    grade = Column(Integer, nullable=False)
    credit = Column(Integer, nullable=False)
    day = Column(String(255), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    course_room = Column(String(100), nullable=False)

# CourseTimetable 테이블 정의
class CourseTimetable(Base):
    __tablename__ = "course_timetable"
    course_timetable_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    timetable_id = Column(BigInteger, ForeignKey("timetable.timetable_id"), nullable=False)
    course_id = Column(BigInteger, ForeignKey("course.course_id"), nullable=False)

# CourseReview 테이블 정의
class CourseReview(Base):
    __tablename__ = "course_review"
    course_review_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    course_id = Column(BigInteger, ForeignKey("course.course_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    content = Column(String(255), nullable=False)
