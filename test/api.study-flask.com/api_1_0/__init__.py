#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .apiVersionResource import apiversion_blueprint
from .studentResource import student_blueprint
from .studentSelectedCourseResource import studentselectedcourse_blueprint
from .sysDepartmentInfoResource import sysdepartmentinfo_blueprint
from .teacherResource import teacher_blueprint
from .courseResource import course_blueprint
from .sysClassInfoResource import sysclassinfo_blueprint
from .ssoUserResource import ssouser_blueprint
from .courseArrangementResource import coursearrangement_blueprint
from .sysCollegeInfoResource import syscollegeinfo_blueprint
from .adminResource import admin_blueprint
from .vStudentCourseScoreResource import vstudentcoursescore_blueprint


def init_router(app):
    from api_1_0.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="/api_1_0")

    # student blueprint register
    from api_1_0.studentResource import student_blueprint
    app.register_blueprint(student_blueprint, url_prefix="/api_1_0")
    
    # studentSelectedCourse blueprint register
    from api_1_0.studentSelectedCourseResource import studentselectedcourse_blueprint
    app.register_blueprint(studentselectedcourse_blueprint, url_prefix="/api_1_0")
    
    # sysDepartmentInfo blueprint register
    from api_1_0.sysDepartmentInfoResource import sysdepartmentinfo_blueprint
    app.register_blueprint(sysdepartmentinfo_blueprint, url_prefix="/api_1_0")
    
    # teacher blueprint register
    from api_1_0.teacherResource import teacher_blueprint
    app.register_blueprint(teacher_blueprint, url_prefix="/api_1_0")
    
    # course blueprint register
    from api_1_0.courseResource import course_blueprint
    app.register_blueprint(course_blueprint, url_prefix="/api_1_0")
    
    # sysClassInfo blueprint register
    from api_1_0.sysClassInfoResource import sysclassinfo_blueprint
    app.register_blueprint(sysclassinfo_blueprint, url_prefix="/api_1_0")
    
    # ssoUser blueprint register
    from api_1_0.ssoUserResource import ssouser_blueprint
    app.register_blueprint(ssouser_blueprint, url_prefix="/api_1_0")
    
    # courseArrangement blueprint register
    from api_1_0.courseArrangementResource import coursearrangement_blueprint
    app.register_blueprint(coursearrangement_blueprint, url_prefix="/api_1_0")
    
    # sysCollegeInfo blueprint register
    from api_1_0.sysCollegeInfoResource import syscollegeinfo_blueprint
    app.register_blueprint(syscollegeinfo_blueprint, url_prefix="/api_1_0")
    
    # admin blueprint register
    from api_1_0.adminResource import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/api_1_0")
    
    # vStudentCourseScore blueprint register
    from api_1_0.vStudentCourseScoreResource import vstudentcoursescore_blueprint
    app.register_blueprint(vstudentcoursescore_blueprint, url_prefix="/api_1_0")
    
