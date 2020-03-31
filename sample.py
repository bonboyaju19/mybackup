import modules.aws_search as aws_search
import modules.aws_backup as aws_backup
import modules.ec2_stop as ec2_stop
import modules.ec2_start as ec2_start
import modules.utils.logger as logger
import modules.utils.handler as handler
import modules.utils.ec2 as ec2
import modules.utils.rds as rds
import modules.utils.efs as efs

logger = logger.get_logger()
error_type = handler.ErrorType


def offline_backup(key, value, vault_name, iam_role_arn):
    logger.info("オフラインバックアップを開始します")
    try:
        ec2_id_list = aws_search.search_ec2_id_filtered_by_tag(
            key, value)
        rds_id_list = aws_search.search_rds_id_filtered_by_tag(
            key, value)
        efs_id_list = aws_search.search_efs_id_filtered_by_tag(
            key, value)

        ec2_stop.stop_instances(ec2_id_list)

        aws_backup.backup(vault_name, iam_role_arn,
                          ec2_id_list, rds_id_list, efs_id_list)

        ec2_start.start_instances(ec2_id_list)
    except Exception as e:
        handler.handle_error(error_type.OTHER_UNKNOWN_ERROR, e)


if __name__ == '__main__':
    offline_backup("KEY", "VALUE", "VAULT_NAME", "IAM_ROLE_ARN")
