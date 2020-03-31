from modules.utils import logger
from modules.utils import handler
import boto3

logger = logger.get_logger()
error_type = handler.ErrorType

ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')
efs_client = boto3.client('efs')


def search_ec2_id_filtered_by_tag(key, value):
    logger.info("[key: %s, value: %s]でEC2を検索します" % (key, value))
    try:
        # tagでフィルターをして、EC2の一覧を取得する
        instance_list = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:' + key,
                    'Values': [value]
                }
            ]
        )["Reservations"][0]["Instances"]
        logger.debug(instance_list)
        ec2_id_list = [i.get("InstanceId") for i in instance_list]
        logger.info(ec2_id_list)
        return ec2_id_list
    except Exception as e:
        handler.handle_error(error_type.AWS_SEARCH_EC2_UNKNOWN_ERROR, e)


def search_rds_id_filtered_by_tag(key, value):
    logger.info("[key: %s, value: %s]でRDSを検索します" % (key, value))
    try:
        database_list = rds_client.describe_db_instances()["DBInstances"]
        for db in database_list[:]:
            # RDSのAPIはタグとDB情報の一覧を取得することができないため、DB毎にタグ情報を取得し、確認する
            tag_list = rds_client.list_tags_for_resource(
                ResourceName=db["DBInstanceArn"]
            )["TagList"]
            # 指定されたkey, valueが見つからない場合はリストから除外する
            tag = [tag for tag in tag_list if (key, value) in tag.items()]
            if tag is None:
                database_list.remove(db)
        logger.debug(database_list)
        rds_id_list = [d.get("DBInstanceIdentifier") for d in database_list]
        logger.info(rds_id_list)
        return rds_id_list
    except Exception as e:
        handler.handle_error(error_type.AWS_SEARCH_RDS_UNKNOWN_ERROR, e)


def search_efs_id_filtered_by_tag(key, value):
    logger.info("[key: %s, value: %s]でEFSを検索します" % (key, value))
    try:
        filesystem_list = efs_client.describe_file_systems()["FileSystems"]
        for fs in filesystem_list[:]:
            # 指定されたkey, valueが見つからない場合はリストから除外する
            tag = [tag for tag in fs["Tags"] if (key, value) in tag.items()]
            if tag is None:
                filesystem_list.remove(fs)
        logger.debug(filesystem_list)
        efs_id_list = [f.get("FileSystemId") for f in filesystem_list]
        logger.info(efs_id_list)
        return efs_id_list
    except Exception as e:
        handler.handle_error(error_type.AWS_SEARCH_EFS_UNKNOWN_ERROR, e)
