import os
from dotenv import load_dotenv
from application import create_app
from application.configuration import DevelopmentConfiguration, ProductionConfiguration


load_dotenv()

is_production = os.getenv('PRODUCTION', 'True') == 'True'
configuration = ProductionConfiguration if is_production else DevelopmentConfiguration()

app = create_app(configuration)

if __name__ == '__main__':
  app.run(debug=not is_production)
  # app.run()
