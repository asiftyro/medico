import os
from dotenv import load_dotenv
from application import create_app
from application.configuration import DevelopmentConfiguration, ProductionConfiguration
from application.logging import logger

load_dotenv()

app_host = os.getenv("APP_HOST", "localhost")
app_port = int(os.getenv("APP_PORT", 5000))
is_production = os.getenv("PRODUCTION", "True") == "True"
configuration = ProductionConfiguration if is_production else DevelopmentConfiguration()

app = create_app(configuration)

if __name__ == "__main__":
    logger.info("Starting Application")
    logger.info(f"Production: {is_production}")
    logger.info(f"Host: {app_host}")
    logger.info(f"Port: {app_port}")
    app.run(host=app_host, port=app_port, debug=not is_production)
