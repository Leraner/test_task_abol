import os

import settings


class Commands:
    def create_default_folders(self):
        for instance, folder in settings.FILES.items():
            if not os.path.exists(folder):
                os.makedirs(folder)
