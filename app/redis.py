from redis import Redis
from app import config

redis = Redis(config.redis_host, config.redis_port, config.redis_db)
