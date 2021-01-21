import environs

env = environs.Env()

DATABASE_URI = env.str("DATABASE_URI", "")
