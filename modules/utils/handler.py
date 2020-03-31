from . import logger
from enum import Enum
import sys

logger = logger.get_logger()


class ErrorType(Enum):
    '''
    命名規則
    [モジュール名]_[エラー概要]
    '''

    # aws.py
    AWS_EC2_DESCRIBE_FAILED = "インスタンスの詳細を取得中にエラーが発生しました"
    AWS_EC2_DESCRIBE_STATUS_FAILED = "インスタンスのステータスを取得中にエラーが発生しました"
    AWS_EC2_STOP_FAILED = "インスタンス停止中にエラーが発生しました"
    AWS_EC2_START_FAILED = "インスタンス起動中にエラーが発生しました"
    AWS_RDS_DESCRIE_FAILED = "RDSの情報を取得中にエラーが発生しました"
    AWS_EFS_DESCRIBE_FAILED = "EFSの情報を取得中にエラーが発生しました"
    AWS_BACKUP_START_JOB_FAILED = "バックアップジョブ開始中にエラーが発生しました"
    AWS_BACKUP_DESCRIBE_FAILED = "バックアップジョブ取得中にエラーが発生しました"

    # ec2.py
    EC2_BACKUP_JOB_ID_NOT_FOUND = "EC2のbackup_job_idが見つかりません"
    EC2_BACKUP_JOB_FAILED = "EC2のバックアップジョブが失敗しました"

    # rds.py
    RDS_BACKUP_JOB_ID_NOT_FOUND = "RDSのbackup_job_idが見つかりません"
    RDS_BACKUP_JOB_FAILED = "RDSのバックアップジョブが失敗しました"

    # efs.py
    EFS_BACKUP_JOB_ID_NOT_FOUND = "EFSのbackup_job_idが見つかりません"
    EFS_BACKUP_JOB_FAILED = "EFSのバックアップジョブが失敗しました"

    # aws_backup.py
    AWS_BACKUP_UNKNOWN_ERROR = "バックアップ取得中に不明なエラーが発生しました"

    # aws_search.py
    AWS_SEARCH_EC2_UNKNOWN_ERROR = "EC2の検索中に不明なエラーが発生しました"
    AWS_SEARCH_RDS_UNKNOWN_ERROR = "RDSの検索中に不明なエラーが発生しました"
    AWS_SEARCH_EFS_UNKNOWN_ERROR = "EFSの検索中に不明なエラーが発生しました"

    # ec2_start.py
    EC2_START_UNKNOWN_ERROR = "EC2の起動中に不明なエラーが発生しました"

    # ec2_stop.py
    EC2_STOP_UNKNOWN_ERROR = "EC2の起動中に不明なエラーが発生しました"

    # その他
    OTHER_UNKNOWN_ERROR = "不明なエラーが発生しました"


def handle_error(error_type, exception="", message=""):
    logger.error("%s:%s" % (error_type.name, error_type.value))

    # exceptionが空でなければエラー出力
    if not exception:
        logger.exception(exception)
    
    # messageが空でなければエラー出力
    if not message:
        logger.error(message)

    # 異常コードで終了させる
    sys.exit(1)
