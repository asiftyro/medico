import os
from dotenv import load_dotenv
from application import create_app
from application.configuration import DevelopmentConfiguration, ProductionConfiguration, StagingConfiguration
from application.logging import logger

load_dotenv()

app_host = os.getenv("APP_HOST", "localhost")
app_port = int(os.getenv("APP_PORT", 5000))


# Values: 0 = debug, 1 = production, 2 = statging
run_mode = os.getenv("PRODUCTION", "0").strip()

configuration = None

if run_mode == "0":
    configuration = DevelopmentConfiguration
elif run_mode == "1":
    configuration = ProductionConfiguration
elif run_mode == "2":
    configuration = StagingConfiguration


is_debug = configuration.DEBUG

app = create_app(configuration)

if __name__ == "__main__":
    logger.info("Application Bootup started...")
    logger.info(f"Boot mode: {configuration()}")
    logger.info(f"Debug: {is_debug}")
    logger.info(f"Host: {app_host}")
    logger.info(f"Port: {app_port}")
    app.run(host=app_host, port=app_port, debug=is_debug)
