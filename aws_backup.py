import ec2
import efs
import rds
import boto3
import logger

logger = logger.Logger()

ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')
efs_client = boto3.client('efs')


def search_ec2_filtered_by_tag(key, value):
    return ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'tag:' + key,
                'Values': [value]
            }
        ]
    )["Reservations"][0]["Instances"]

def search_rds_filtered_by_tag(key, value):
    database_list = rds_client.describe_db_instances()["DBInstances"]
    for db in database_list[:]:
        tag_list = rds_client.list_tags_for_resource(
            ResourceName = db["DBInstanceArn"]
        )["TagList"]
        # 指定されたkey, valueが見つからない場合はリストから除去する
        tag = [tag for tag in tag_list if (key, value) in tag.items()]
        if tag is None:
            database_list.remove(db)
    return database_list


def search_efs_filtered_by_tag(key, value):
    filesystem_list = efs_client.describe_file_systems()["FileSystems"]
    for fs in filesystem_list[:]:
        # 指定されたkey, valueが見つからない場合はリストから除去する
        tag = [tag for tag in fs["Tags"] if (key, value) in tag.items()]
        if tag is None:
            filesystem_list.remove(fs)
    return filesystem_list


def online_backup(tenant_name, vault_name, iam_role_arn):
    logger.info("オンラインバックアップを開始します")

    try:
        logger.info("バックアップ対象を取得します")
        instances = search_ec2_filtered_by_tag("tenant", tenant_name)
        databases = search_rds_filtered_by_tag("tenant", tenant_name)
        filesystems = search_efs_filtered_by_tag("tenant", tenant_name)

        logger.info("バックアップ対象をインスタンス化します")
        instance_objects = []
        database_objects = []
        filesystem_objects = []
        for i in instances:
            instance_objects.append(ec2.Instance(i["InstanceId"]))
        for d in databases:
            database_objects.append(rds.Database(d["DBInstanceIdentifier"]))
        for f in filesystems:
            filesystem_objects.append(efs.FileSystem(f["FileSystemId"]))

        logger.info("バックアップを開始します")
        for i in instance_objects:
            i.create_backup(vault_name, iam_role_arn)
        for d in database_objects:
            d.create_backup(vault_name, iam_role_arn)
        for f in filesystem_objects:
            f.create_backup(vault_name, iam_role_arn)

        logger.info("バックアップの完了確認をします")
        for i in instance_objects:
            i.wait_for_completed()
        for d in database_objects:
            d.wait_for_completed()
        for f in filesystem_objects:
            f.wait_for_completed()

        logger.info("オンラインバックアップが完了しました")
    except Exception as e:
        logger.error("オンラインバックアップ中にエラーが発生しました", e)
