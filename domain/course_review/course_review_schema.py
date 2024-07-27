# schema: api 명세서를 가지고 필요한 재료들을 채워넣는 것

import datetime

from pydantic import BaseModel, Field

class CourseReview(BaseModel):
    rating: float
    content: str

class CourseReviews(BaseModel):
    courseName: str
    courseReviews: list[CourseReview]

