from distutils.dir_util import copy_tree
import os
from configparser import ConfigParser
from masque.model import Base
from masque.model.image import Image
import sqlalchemy
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
    s3_bucket_folder = config_parser.get('aws', 'folder')
    mysql_user = config_parser.get('mysql', 'mysql_user')
    mysql_password = config_parser.get('mysql', 'mysql_password')
    mysql_host = config_parser.get('mysql', 'mysql_host')
    mysql_port = config_parser.get('mysql', 'mysql_port')
    mysql_db = config_parser.get('mysql', 'mysql_db')

    engine = sqlalchemy.create_engine(
        'mysql+mysqlconnector://' + mysql_user + ':' + mysql_password + '@' + mysql_host + ':' + mysql_port + '/' + mysql_db,
        echo=True
    )

    Base.metadata.create_all(engine)

    # Create a session
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    to_directory = os.path.join(cwd, 'img')

    optimized_directory = os.path.join(cwd, 'optimized')

    if not os.path.exists(to_directory):
        os.makedirs(to_directory)

    if not os.path.exists(optimized_directory):
        os.makedirs(optimized_directory)

    os.chmod(to_directory, 0o755)
    os.chmod(optimized_directory, 0o755)

    directory_contents = os.listdir(to_directory)
    if len(directory_contents) == 0:
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
            path=aws_bucket + '/' + s3_bucket_folder + '/s_' + filename
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
            path=aws_bucket + '/' + s3_bucket_folder + '/m_' + filename
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
            path=aws_bucket + '/' + s3_bucket_folder + '/l_' + filename
        )

        source.store(
            service='s3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region=aws_region,
            path=aws_bucket + '/' + s3_bucket_folder + '/o_' + filename
        )

        # Add a image record
        image_record = Image(file_name=filename, directory=s3_bucket_folder)
        session.add(image_record)
        session.commit()

        os.remove(file_path)
