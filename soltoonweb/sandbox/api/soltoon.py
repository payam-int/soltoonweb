import docker
import os
from django.conf import settings

dockerClient = docker.from_env()


def compile_code(user_code, output_jar_name):
    user_code_filename = os.path.basename(user_code)
    output_file = os.path.join(settings.SOLTOON_SANDBOX['jar-directory'], output_jar_name)
    output_jar_filename = output_jar_name
    # create output file
    open(output_file, 'w+').close()

    binds = {
        user_code: {'bind': '/code/' + user_code_filename, 'mode': 'ro'},
        output_file: {'bind': '/output/' + output_jar_filename, 'mode': 'ro'}
    }

    tempfs = {
        '/working_dir': 'size=200M'
    }

    environ = {
        'USER_CODE': '',
        'OUTPUT_JAR': '',
        'USER_CODE_MAIN_CLASS': '',
        'USER_CODE': '',
    }
