import pandas as pd
import requests
import streamlit as st
from SemTestSuite import CONFIG, logger
from os import environ
from typing import Dict, List, Tuple, Union

url = CONFIG.get("webservice", "lexibot_url")

st.set_page_config(
    page_title="SemTestSuite",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def get_models() -> List[str]:
    """Get the available models from LexiBot.

    Returns:
        List[str]: The available models.

    """
    response = requests.get(f"{url}/models")
    return response.json()


@st.cache_data
def get_roles() -> List[str]:
    """Get the predefined roles from LexiBot.

    Returns:
        List[str]: The available roles.

    """
    response = requests.get(f"{url}/roles")
    return response.json()


def get_role(role: str, lang: str) -> Dict[str, Union[str, List[str]]]:
    """Get the predefined role instructions from LexiBot.

    Args:
        role (str): The role to get.

    Returns:
        str: The role.

    """
    response = requests.get(f"{url}/role/{role}", params={"lang": lang})
    return response.json()


def new_chat(instructions: str) -> Dict[str, List[Dict[str, str]]]:
    """Start a new chat with LexiBot.

    Args:
        instructinos (str): Initial instructions for the bot to use.

    Returns:
        Dict[str, str | List[Dict[str, str]]]: The response from LexiBot.

    """
    response = requests.get(f"{url}/new_chat", params={"instructions": instructions})
    return response.json()


def get_lexibot_response(
    message: str,
    model: str,
    dialogue: List[Dict[str, str]] = [],
    temperature: float = 1.0,
) -> Tuple[str, List[Dict[str, str]]]:
    """Get a response from LexiBot.

    Args:
        message (str): The message to send to LexiBot.
        dialogue (List[Dict[str, str]]): The dialogue so far.

    Returns:
        Dict[str, str | List[Dict[str, str]]]: The response from LexiBot.

    """
    print("Sending message to LexiBot")
    print(f"Message: {message}")
    print(f"Model: {model}")
    print(f"Temperature: {temperature}")
    response = requests.post(
        f"{url}/chat?model={model}&temperature={temperature}",
        json={
            "new_message": message,
            "dialogue": dialogue,
        },
    )
    print(f"Response: {response}")
    print(f"Status code: {response.status_code}")
    if response.status_code != 200:
        return f"Error: response.json()", []
    response = response.json()
    return response["reply"], response["dialogue"]


def get_image_from_prompt(prompt: str) -> List[str]:
    """Get an image from a prompt.

    Args:
        prompt (str): The prompt to use.

    Returns:
        str: The image URL.

    """
    print(prompt)
    response = requests.post(f"{url}/image", params={"prompt": prompt})
    print("return")
    print(response)
    data = response.json()
    print(data)
    print(data.get("image_urls", []))
    if isinstance(data, dict):
        return data.get("image_urls", [])
    else:
        return []


def process_data(data: pd.DataFrame, instructions):
    answers = []
    for row in data.itertuples():
        pass
