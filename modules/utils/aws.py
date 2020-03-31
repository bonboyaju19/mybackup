from . import logger
from . import handler
import boto3

logger = logger.get_logger()
error_type = handler.ErrorType


class Aws:
    def __init__(self):
        logger.debug("Awsクラスを初期化します")
        self.ec2_client = boto3.client('ec2')
        self.backup_client = boto3.client('backup')
        self.efs_client = boto3.client('efs')
        self.rds_client = boto3.client('rds')
        self.session = boto3.session.Session()

    def get_region(self):
        return self.session.region_name

    def describe_instances(self, instance_id):
        logger.debug("インスタンスの詳細を取得します")
        try:
            response = self.ec2_client.describe_instances(
                InstanceIds=[instance_id]
            )
            logger.debug(response)
            return response
        except Exception as e:
            handler.handle_error(error_type.AWS_EC2_DESCRIBE_FAILED, e)

    def describe_instance_status(self, instance_id):
        logger.debug("インスタンスのステータスを取得します")
        try:
            response = self.ec2_client.describe_instance_status(
                InstanceIds=[instance_id]
            )
            logger.debug(response)
            return response
        except Exception as e:
            handler.handle_error(error_type.AWS_EC2_DESCRIBE_STATUS_FAILED, e)

    def stop_instances(self, instance_id):
        try:
            response = self.ec2_client.stop_instances(
                InstanceIds=[instance_id]
            )
            logger.debug(response)
            return response
        except Exception as e:
            handler.handle_error(error_type.AWS_EC2_STOP_FAILED, e)

    def start_instances(self, instance_id):
        try:
            response = self.ec2_client.start_instances(
                InstanceIds=[instance_id]
            )
            logger.debug(response)
            return response
        except Exception as e:
            handler.handle_error(error_type.AWS_EC2_START_FAILED, e)

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
            logger.debug(response)
            return response
        except Exception as e:
            handler.handle_error(error_type.AWS_BACKUP_START_JOB_FAILED, e)

    def describe_backup_job(self, backup_job_id):
        try:
            response = self.backup_client.describe_backup_job(
                BackupJobId=backup_job_id
            )
            logger.debug(response)
            return response
        except Exception as e:
            handler.handle_error(error_type.AWS_BACKUP_DESCRIBE_FAILED, e)

    def describe_db_instances(self, db_instance_id):
        try:
            response = self.rds_client.describe_db_instances(
                DBInstanceIdentifier=db_instance_id
            )
            logger.debug(response)
            return response
        except Exception as e:
            handler.handle_error(error_type.AWS_RDS_DESCRIE_FAILED, e)

    def describe_file_systems(self, file_system_id):
        try:
            response = self.efs_client.describe_file_systems(
                FileSystemId=file_system_id
            )
            logger.debug(response)
            return response
        except Exception as e:
            handler.handle_error(error_type.AWS_EFS_DESCRIBE_FAILED, e)
