import environs

env = environs.Env()

DATABASE_URI = env.str(
    "DATABASE_URI", "postgres://hermes:hermes102030@localhost/hermes"
)
