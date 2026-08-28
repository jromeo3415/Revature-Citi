import boto3
import asyncio
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import DiagnosticLog

BUCKET_NAME = "robopulse-jr"
PREFIX = "diagnostics/"

def list_bucket_diagnostics() -> list[str]:
    s3_client = boto3.client('s3')
    paginator = s3_client.get_paginator("list_objects_v2")

    keys = []

    for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=PREFIX):
        for object in page.get("Contents", []):
            keys.append(f"s3://{BUCKET_NAME}/{object['Key']}")

    return keys
        

async def list_db_diagnostics() -> list[str]:
    async with AsyncSessionLocal() as session:
        statement = select(DiagnosticLog.id, DiagnosticLog.file_url)

        result = await session.execute(statement)
        return result.all()        

async def main() -> None: 
    s3_keys = list_bucket_diagnostics()
    db_keys = await list_db_diagnostics()

    for id, db_key in db_keys:

        if db_key not in s3_keys:
            print(f"Broken - (Diagnostic log ID: {id}, no matching file)")
        else: 
            print(f"Healthy - (Diagnostic log ID: {id})")


if __name__ == "__main__":
    asyncio.run(main())