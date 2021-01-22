import environs

env = environs.Env()

ENVIRONMENT = env.str("ENVIRONMENT", "dev")
DATABASE_URI = env.str(
    "DATABASE_URI", "postgres://hermes:hermes102030@localhost/hermes"
)
