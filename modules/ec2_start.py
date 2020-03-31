from modules.utils import ec2
from modules.utils import logger
from modules.utils import handler

logger = logger.get_logger()
error_type = handler.ErrorType


def start_instances(ec2_id_list=[]):
    logger.info("EC2の起動を開始します")
    logger.debug(ec2_id_list)

    try:
        logger.info("対象のEC2をインスタンス化します")
        instance_list = []
        for ec2_id in ec2_id_list:
            instance_list.append(ec2.Instance(ec2_id))

        logger.info("EC2の起動を実行します")
        for i in instance_list:
            i.start()

        logger.info("EC2の起動完了確認を行います")
        for i in instance_list:
            i.wait_for_started()

        logger.info("EC2の起動が完了しました")
    except Exception as e:
        handler.handle_error(error_type.EC2_START_UNKNOWN_ERROR, e)
