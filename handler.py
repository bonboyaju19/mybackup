import aws_backup

if __name__ == '__main__':
    aws_backup.online_backup("TENANT_NAME", "VAULT_NAME", "IAM_ROLE_ARN")
    