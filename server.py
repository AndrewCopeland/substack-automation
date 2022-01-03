import backend
import os
import app
import time

def main():
    # create the config and validate all environment variables are present
    config = {
        'FINAGE_API_KEY': os.environ['FINAGE_API_KEY'],
        'SUBSTACK_EMAIL': os.environ['SUBSTACK_EMAIL'],
        'SUBSTACK_PASSWORD': os.environ['SUBSTACK_PASSWORD'],
        'SUBSTACK_PUBLISH_URL': os.environ['SUBSTACK_PUBLISH_URL'],
        'CHROME_DRIVER_PATH': os.environ['CHROME_DRIVER_PATH']
    }

    # run the application with provided configuration
    app.run(config)

if __name__ == "__main__":
    main()