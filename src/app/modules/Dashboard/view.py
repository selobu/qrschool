from flask import current_app as app
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.apitools import FilterParams, allow_to_change_output_fmt

from .pdModels import attendance_per_day, today_abscent, attendancce_group_per_day
from .controller import (
    DailyAttendanceController,
    DailyAbscentController,
    TodayAbscentController,
    AttendanceGroupPerDayController,
)

api = app.api  # type: ignore
ns_dashboard = api.namespace("dashboard", description="Admin dashboard")

parser = FilterParams().add_outputfmt()


@ns_dashboard.route("/dailyattendance")
class DailyAttendance(Resource):
    """Daily attendance"""

    @allow_to_change_output_fmt(parser, keyword="usrs")
    @ns_dashboard.doc("Get daily attendace list by date")
    @ns_dashboard.marshal_list_with(attendance_per_day, code=200)
    @ns_dashboard.expect(parser.paginate_model)
    @jwt_required()
    def get(self):
        """Return the attendance list of the last day"""
        return DailyAttendanceController.get(parser)


@ns_dashboard.route("/dailyabscent")
class DailyAbscent(Resource):
    """Weekly attendance"""

    @allow_to_change_output_fmt(parser, keyword="usrs")
    @ns_dashboard.doc("Get daily abscent list by date")
    @ns_dashboard.marshal_with(attendance_per_day, code=200)
    @ns_dashboard.expect(parser.paginate_model)
    @jwt_required()
    def get(self):
        """Return the abscent list of the last day"""
        return DailyAbscentController.get(parser)


@ns_dashboard.route("/todayabscent")
class TodaysAbscentStudent(Resource):
    """Missign students reported today."""

    @allow_to_change_output_fmt(parser, keyword="usrs")
    @ns_dashboard.doc("User's information")
    @ns_dashboard.marshal_with(today_abscent, code=200)
    @ns_dashboard.expect(parser.paginate_model)
    @jwt_required()
    def get(self):
        """Retorna todos los usuarios3
        límite actual 50 usuarios
        """
        return TodayAbscentController.get(parser)


@ns_dashboard.route("/attendancepergradetoday")
class AttendancePerGradeToday(Resource):
    """Attendance amount per grade today."""

    @allow_to_change_output_fmt(parser, keyword="usrs")
    @ns_dashboard.doc("User's information")
    @ns_dashboard.marshal_with(attendancce_group_per_day, code=200)
    @ns_dashboard.expect(parser.paginate_model)
    @jwt_required()
    def get(self):
        """get the attendance amount per grade today"""
        return AttendanceGroupPerDayController.get(parser)
