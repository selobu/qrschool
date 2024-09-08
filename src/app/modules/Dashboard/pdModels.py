from flask_restx.fields import String, Integer, Date
from flask import current_app


attendance_per_day = current_app.api.model(
    "DailyAttendance", {"Date": Date(), "Count": Integer()}
)

today_abscent = current_app.api.model(
    "TodayAbscent",
    {"Date": Date(), "grade": String(), "name": String(), "last_name": String()},
)

attendancce_group_per_day = current_app.api.model(
    "AttendanceGrupPerDay",
    {
        "Date": Date(),
        "gradeid": String(),
        "grade": String(),
        "attendance": String(),
    },
)
