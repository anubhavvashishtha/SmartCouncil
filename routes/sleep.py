from routes.agent_template import create_agent
from dotenv import load_dotenv
import os

load_dotenv()

app = create_agent("Sleep", os.getenv("Sleep"))