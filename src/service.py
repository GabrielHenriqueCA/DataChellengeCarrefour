from typing import Any, Dict, List
import tweepy
from src.conection import collection_trends
from src.constants import BRAZIL_WOE_ID
from src.tokens import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET


def _get_trends(woe_id: BRAZIL_WOE_ID, api: tweepy.API) -> List[Dict[str, Any]]:
    """Pega os Trending topics da api do twitter.
    Args:
        woe_id (int): Identificador de Localização.
    Returns:
        List[Dict[str, Any]]: Lista de Trends.
    """
    trends = api.trends_place(woe_id)

    return trends[0]["trends"]


def get_trends() -> List[Dict[str, Any]]:
    trends = collection_trends.find({})
    return list(trends)


def save_trends() -> None:
    """Pega as Trends e Salva no MongoDB."""
    auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    trends = _get_trends(woe_id=BRAZIL_WOE_ID, api=api)
    collection_trends.insert_many(trends)
