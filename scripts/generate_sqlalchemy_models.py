# from flask import json
from sqlalchemy_data_model_visualizer import (
    generate_data_model_diagram,
    add_web_font_and_interactivity,
)
from pathlib import Path
from sys import path as syspath

cpath = Path(__file__).parent.parent

if (pth := str(cpath / "src")) not in syspath:
    syspath.append(pth)

from app import create_app, config  # noqa:E402

Devconfig = config.DevelopmentConfig
Devconfig.SERVER_NAME = "localhost"

app = create_app(Devconfig)
with app.app_context():
    Tb = app.Tb
    models = list()
    models = [getattr(Tb, prop) for prop in dir(Tb) if not prop.startswith("_")]
    # models = [GenericUser, Customer, ContentCreator, UserSession, FileStorage, ServiceRequest, GenericAuditLog, GenericFeedback, GenericAPIKey, GenericNotification, GenericAPICreditLog, GenericSubscriptionType, GenericSubscription, GenericSubscriptionUsage, GenericBillingInfo]
    output_file_name = "my_data_model_diagram"
    generate_data_model_diagram(models, output_file_name)
    add_web_font_and_interactivity(
        "my_data_model_diagram.svg", "my_interactive_data_model_diagram.svg"
    )
