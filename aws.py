import boto3
import logger

logger = logger.Logger()


class Aws:
    def __init__(self):
        logger.info("Awsクラスを初期化します")
        self.ec2_client = boto3.client('ec2')
        self.backup_client = boto3.client('backup')
        self.efs_client = boto3.client('efs')
        self.rds_client = boto3.client('rds')
        self.session = boto3.session.Session()

    def get_region(self):
        return self.session.region_name

    def describe_instances(self, instance_id):
        logger.info("インスタンスの詳細を取得します")
        try:
            response = self.ec2_client.describe_instances(
                InstanceIds=[instance_id]
            )
            logger.info(response)
            return response
        except Exception as e:
            logger.error("インスタンスの詳細を取得中にエラーが発生しました", e)

    def describe_instance_status(self, instance_id):
        logger.info("インスタンスのステータスを取得します")
        try:
            response = self.ec2_client.describe_instance_status(
                InstanceIds=[instance_id]
            )
            logger.info(response)
            return response
        except Exception as e:
            logger.error("インスタンスのステータスを取得中にエラーが発生しました", e)

    def stop_instances(self, instance_id):
        try:
            response = self.ec2_client.stop_instances(
                InstanceIds=[instance_id]
            )
            logger.info(response)
            return response
        except Exception as e:
            logger.error("インスタンス停止中にエラーが発生しました", e)

    def start_instances(self, instance_id):
        try:
            response = self.ec2_client.start_instances(
                InstanceIds=[instance_id]
            )
            logger.info(response)
            return response
        except Exception as e:
            logger.error("インスタンス起動中にエラーが発生しました", e)

    def start_backup_job(self, vault_name, source_arn, iam_role_arn, retention_period=7):
        try:
            response = self.backup_client.start_backup_job(
                BackupVaultName=vault_name,
                ResourceArn=source_arn,
                IamRoleArn=iam_role_arn,
                Lifecycle={
                    'DeleteAfterDays': retention_period
                }
            )
            logger.info(response)
            return response
        except Exception as e:
            logger.error("バックアップジョブ開始中にエラーが発生しました", e)

    def describe_backup_job(self, backup_job_id):
        try:
            response = self.backup_client.describe_backup_job(
                BackupJobId=backup_job_id
            )
            logger.info(response)
            return response
        except Exception as e:
            logger.error("バックアップジョブ取得中にエラーが発生しました", e)

    def describe_file_systems(self, file_system_id):
        try:
            response = self.efs_client.describe_file_systems(
                FileSystemId=file_system_id
            )
            logger.info(response)
            return response
        except Exception as e:
            logger.error("EFSの情報を取得中にエラーが発生しました", e)

    def describe_db_instances(self, db_instance_id):
        try:
            response = self.rds_client.describe_db_instances(
                DBInstanceIdentifier=db_instance_id
            )
            logger.info(response)
            return response
        except Exception as e:
            logger.error("RDSの情報を取得中にエラーが発生しました", e)