import discord.ext.test as dpytest
from dotenv import load_dotenv
import os
from pathlib import Path
import pytest
import sys

# import senpy from ../src
sys.path.append(str(Path(__file__).parent.parent / "src"))
import sen as senpy


load_dotenv()


@pytest.fixture
def bot():
    b = senpy.create_bot()
    dpytest.configure(b)
    return b


@pytest.fixture
def prefix():
    return os.environ["DEFAULT_COMMAND_PREFIX"]
