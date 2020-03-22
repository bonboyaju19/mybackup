import time
import logger
import aws

logger = logger.Logger()
aws = aws.Aws()


class FileSystem:
    def __init__(self, id):
        logger.info("FileSystemクラスを初期化します")
        self.id = id
        self.set_detail()
        logger.info(self.detail)

    def set_detail(self):
        response = aws.describe_file_systems(self.id)
        self.account_id = response["FileSystems"][0]["OwnerId"]
        self.region = aws.get_region()
        self.arn = "arn:aws:elasticfilesystem:" + self.region + \
            ":" + self.account_id + ":file-system/" + self.id
        self.detail = response

    def create_backup(self, vault_name, iam_role_arn):
        logger.info("バックアップを作成します: " + self.id)
        self.backup_job_id = aws.start_backup_job(
            vault_name,
            self.arn,
            iam_role_arn
        )["BackupJobId"]
        self.set_backup_job(self.backup_job_id)

    def set_backup_job(self, backup_job_id):
        self.backup_job_id = backup_job_id
        logger.info("backup_job_id: " + self.backup_job_id)

    def has_completed(self):
        if self.backup_job_id is None:
            logger.warn("backup_job_idが見つかりません")
            return False
        status = aws.describe_backup_job(self.backup_job_id)["State"]
        if status == "COMPLETED":
            logger.info("バックアップジョブが成功しました:" + self.backup_job_id)
            return True
        elif status == "FAILED":
            logger.warn("バックアップジョブが失敗しました:" + self.backup_job_id)
            return False
        else:
            return False

    def wait_for_completed(self, interval=30, retries=30):
        logger.info("バックアップ作成が完了するまで待機します")
        for r in range(retries):
            if self.has_completed():
                logger.info("バックアップ作成が完了しました")
                return True
            else:
                logger.info("リトライ回数: " + str(r))
                time.sleep(interval)
        logger.warn("リトライ回数の上限を超過しました")
        return False
