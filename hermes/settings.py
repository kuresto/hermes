import environs

env = environs.Env()

ENVIRONMENT = env.str("ENVIRONMENT", "dev")
DATABASE_URL = env.str(
    "DATABASE_URL", "postgres://hermes:hermes102030@localhost/hermes"
)
