from app.api import create_app
from app.config import MySettings
from app.logger import CustomLogger
from app.persistence.sqlalchemy.constants import init_mapper

init_mapper()
CustomLogger.setup_logger()


app = create_app()
lg = CustomLogger.get_logger()
lg.info("🤖🚀✨ %s Backend Started 🤖🚀✨", MySettings.ENVIRONMENT.name)
