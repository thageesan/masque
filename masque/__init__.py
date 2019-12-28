from distutils.dir_util import copy_tree
import os
from configparser import ConfigParser
import tinify

cwd = os.getcwd()


def create_app(config_filename=None):
    config_parser = ConfigParser(os.environ)
    config_path = os.path.join(cwd, config_filename)
    config_parser.read(config_path)

    from_directory = config_parser.get('img', 'img_directory')
    tinify.key = config_parser.get('tinypng', 'api_key')

    aws_access_key_id = config_parser.get('aws', 'aws_access_key_id')
    aws_secret_access_key = config_parser.get('aws', 'aws_secret_access_key')
    aws_region = config_parser.get('aws', 'region')
    aws_bucket = config_parser.get('aws', 'bucket')

    to_directory = os.path.join(cwd, 'img')

    optimized_directory = os.path.join(cwd, 'optimized')

    if not os.path.exists(to_directory):
        os.makedirs(to_directory)

    if not os.path.exists(optimized_directory):
        os.makedirs(optimized_directory)

    os.chmod(to_directory, 0o755)
    os.chmod(optimized_directory, 0o755)

    copy_tree(from_directory, to_directory)

    for filename in os.listdir(to_directory):
        file_path = os.path.join(to_directory, filename)
        print(file_path)
        source = tinify.from_file(file_path)
        resized_small = source.resize(
            method='scale',
            width=640
        )
        resized_small.store(
            service='s3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region=aws_region,
            path=aws_bucket + '/s_' + filename
        )

        resized_medium = source.resize(
            method='scale',
            width=1007
        )
        resized_medium.store(
            service='s3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region=aws_region,
            path=aws_bucket + '/m_' + filename
        )

        resized_large = source.resize(
            method='scale',
            width=1920
        )
        resized_large.store(
            service='s3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region=aws_region,
            path=aws_bucket + '/l_' + filename
        )

        source.store(
            service='s3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region=aws_region,
            path=aws_bucket + '/o_' + filename
        )
