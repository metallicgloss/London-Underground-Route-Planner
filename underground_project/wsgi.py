import os
import sys
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

# Import paths to allow script to include other folders.
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../"
        )
    )
)
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../underground_project"
        )
    )
)
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../underground_route_planner"
        )
    )
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'underground_project.settings')
application = StaticFilesHandler(get_wsgi_application())
