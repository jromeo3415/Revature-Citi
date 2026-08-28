'''
Robopulse Command Center Day 8
Uploads a diagnostic report file to S3 using the boto3 SDK, then creates
a matching DiagnosticLog() row (Day 3's async ORM setup) pointing at
the real S3 URL, thus fulfilling problem statement's storage architecture
for the first time. 
'''

import asyncio
import boto3

from app.database import AsyncSessionLocal
from app.models import DiagnosticLog

BUCKET_NAME = "robopulse-jr"
LOCAL_FILE_PATH = "scripts/sample_diagnostic.txt"

# S3 key is a path within the S3 bucket where the file will be stored
S3_KEY = "diagnostics/rx1001-002.txt"

def upload_to_s3() -> str:
    s3_client = boto3.client("s3")
    s3_client.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, S3_KEY)
    return f"s3://{BUCKET_NAME}/{S3_KEY}"

async def record_diagnostic_log(file_url: str) -> None:
    async with AsyncSessionLocal() as session:

        log = DiagnosticLog(
        mission_id=1,
        file_url=file_url,
        notes="Uploaded via the Day 8 boto3 demo script"
        ) 

        session.add(log)
        await session.commit()
        await session.refresh(log)
        print(f"Created DiagnosticLog id={log.id}, file_url={log.file_url}")

async def main() -> None:
    file_url = upload_to_s3()
    print(f"Uploading to {file_url!r}")
    await record_diagnostic_log(file_url)

if __name__ == "__main__":
    asyncio.run(main())