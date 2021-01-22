import environs

env = environs.Env()

ENVIRONMENT = env.str("ENVIRONMENT", "dev")
DATABASE_URL = env.str(
    "DATABASE_URL",
    "postgres://postgres:[Iw2bt1]@database-1.cf9nsk37vfod.us-east-2.rds.amazonaws.com/postgres",
)
