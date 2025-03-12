import subprocess
import asyncio

from database import connection as conn

db = conn.Database()

backend_commands = ["fastapi dev main.py"]

frontend_commands = [
    "cd frontend",
    "npm run dev"
]

def run_commands(commands):
    process = subprocess.Popen(" && ".join(commands), shell=True)
    return process

async def main():
    await db.async_main()

    backend_process = run_commands(backend_commands)
    frontend_process = run_commands(frontend_commands)

    backend_process.wait()
    frontend_process.wait()

if __name__ == "__main__":
    asyncio.run(main())
