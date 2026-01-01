import json, os, hashlib
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage, FunctionMessage
from langchain_community.chat_models import ChatOllama, ChatOpenAI

#nachricht -> feminine

KI_MODELL = os.getenv("KI_MODELL")
BIST_OLLAMA = False if "false" in os.getenv("BIST_OLLAMA").lower() else True

if BIST_OLLAMA:
    llm = ChatOllama(
        model= KI_MODELL,
        temperature=0.2
    )
else:
    llm = ChatOpenAI(
        model=KI_MODELL,
        temperature=1,
    )

def nachricht_an_gesprach_senden(nachricht, gesprach : list[BaseMessage]):
    benutzer_nachricht = HumanMessage(nachricht)

    gesprach.append(benutzer_nachricht)

    ki_antwort = llm.invoke(gesprach)

    gesprach.append(ki_antwort)

    return gesprach

# def nachricht_erklaren(nachricht)




