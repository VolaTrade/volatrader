from decouple import Config, RepositoryEnv

default_if_blank = lambda env_var, default: default if env_var.strip() == "" else default

config = Config(RepositoryEnv("config.env"))
SERVER_PORT: int = int(default_if_blank(config("SERVER_PORT"), 9000))
MAX_THREADS: int = int(default_if_blank(config("MAX_THREADS"), 10))
