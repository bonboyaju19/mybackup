from modules.utils import ec2
from modules.utils import rds
from modules.utils import efs
from modules.utils import logger
from modules.utils import handler

logger = logger.get_logger()
error_type = handler.ErrorType


def backup(vault_name, iam_role_arn, ec2_id_list=[], rds_id_list=[], efs_id_list=[]):
    logger.info("バックアップを開始します")

    try:
        logger.info("バックアップ対象をインスタンス化します")
        instance_list = []
        database_list = []
        filesystem_list = []

        for ec2_id in ec2_id_list:
            instance_list.append(ec2.Instance(ec2_id))
        for rds_id in rds_id_list:
            database_list.append(rds.Database(rds_id))
        for efs_id in efs_id_list:
            filesystem_list.append(efs.FileSystem(efs_id))

        logger.info("バックアップの取得を開始します")
        for i in instance_list:
            i.create_backup(vault_name, iam_role_arn)
        for d in database_list:
            d.create_backup(vault_name, iam_role_arn)
        for f in filesystem_list:
            f.create_backup(vault_name, iam_role_arn)

        logger.info("バックアップの完了確認をします")
        for i in instance_list:
            i.wait_for_completed()
        for d in database_list:
            d.wait_for_completed()
        for f in filesystem_list:
            f.wait_for_completed()

        logger.info("バックアップが完了しました")

    except Exception as e:
        handler.handle_error(error_type.AWS_BACKUP_UNKNOWN_ERROR, e)
