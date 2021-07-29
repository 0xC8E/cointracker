# cointracker 
_by JC Coto_

## Overview
This repo contains a sample demo API for transaction management. It's fairly simple, but it implements some nice features, like:
- A simple structure that's quite hackable. Adding endpoint support should be quite easy to do (add a database model, set up an API model definition and then hook up the queries up to the API app).
- A custom generator for fixture data to enable prototyping. Using some real-ish data (BTC addresses), there's a handy command to populate a database schema with real-looking data to build out new features. It's also idempotent, so it can be run as many times as necessary.
- FastAPI-based API. This includes both typing support, which incorporates automatically-generated documentation support. Basically, set up the API with the proper returning models, and there's a `/docs` page that generates interactive documentation (so it's also like a simple admin interface!).
- Docker-compose setup for database.
- Some handy scripts to make running the important tasks simple.
- Poetry support for dependency management (this probably shouldn't be a big deal, but in the Python world easy dependency management is kinda iffy).

## Instructions
There's 4 main scripts that will come in handy when running this, in the `scripts` directory. In summary:
1. `start_db.sh` will set up a Docker Compose service with Postgres to configure a database, which the API and fixture generator will use.
2. `db_client.sh` is a handy shortcut to connect to the database using `psql`. The password is `postgres`.
3. `run_api.sh` launches the API in a Uvicorn (an asychronous analog to Gunicorn) server and sets up auto-reloading. The app will be hosted at `http://localhost:8000/`. Docs are available at `http://localhost:8000/docs`.
4. `add_fixtures.sh` will generate some random-ish data to demo on the API.

## General architecture
![Architecture overview](https://cdn.zappy.app/b97f1a544579bb3927079e0e947c5cdc.png)
The architecture of this demo system is pretty standard. It's a multi-layer system, where the front-end is a FastAPI headless server(*) (i.e. there is no UI), which includes automatic validation and marshaling with typed responses. The application layer is included in the endpoint controllers (as, again, this is a really simple app), mostly visible in filtering rules applied to data queried from the DB. For the data access layer, it's built with SQLAlchemy's fantastic table support (so, no ORM), hooked into an asynchronous PostgreSQL driver to tie into FastAPI's async support.

* The exception to the UI point mentioned above is that FastAPI generates OpenAPI-compatible documentation based on the response types specified for an endpoint, in a nice UI that can function as a very simple admin interface.

## Launch plan
There's some really important parts missing to this before it would be production-ready. I'll highlight the major points here.

### 1. Authentication
This is an absolute MUST. User privacy is critically important, and it's our duty to do the utmost to safeguard it. In terms of authentication, I would incorporate support with a good authentication vendor (I've used Okta in the past, and it's worked well), mostly based on the team's current workflow and setup. My recommendation here would be to implement as little as possible of the authentication system, and leave it to the experts (or, if the business merits it, become an expert to build it, but that's a pretty significant decision to make).

### 2. CI/CD
There's no automated testing set up at this point. This is intentional for two reasons:  - there's always a cost associated with testing, so it's important to be deliberate about what tests to add to a project (and in this phase of development, it doesn't seem like tests would add a lot of value);
- integration tests would be the most valuable here, most likely, and that would require more context about the system to implement properly.

Given that, however, I would prioritize nailing down specific requirements and use cases to then derive tests from them, and try to be very deliberate about really valuable tests. After that, I'd dedicate time to configure a good continuous delivery pipeline.

### 3. Monitoring
This is another critical component to doing a proper launch, but it's also one where it's very easy to get into a scenario where there's so much data there's little actionable information. Here, I would either seek to implement monitoring according to the team's goals for delivery (say, from an SLA or some other more formal definition), if there are some, or I would seek to do a phased roll-out and get statistics to at least have a good baseline for critical performance metrics, and set monitors based on those.

There are some critical places where I would focus monitoring, like retrieving transaction history or making blockchain API requests (not implemented here, but likely necessary in production).

### 4. Feedback
Context is king. There's likely to be things that I missed and that are necessary to make a better product, so I'd rely on my team and on customer feedback to make sure that we're delivering the value they actually need.

### 5. Miscellaneous
There's tons of other smaller improvements I would make:
- Environment variables for configuration data (like DB URL)
- Add better debugging support, according to the team's needs
- Linting/formatting (I use `black`, but the team might use something else)
- I'd probably include API versioning from the get-go, and add data migration support
- Better secret support (and better secrets!)


## Closing notes
I debated between building a system to shard and replicate data automatically, but thinking through it further it seemed like there was going to be less demoable value, and if I tried to add more bells and whistles, I wouldn't get a good solution out. This seemed like a good tradeoff, and I'm happy to discuss it further!

Thanks for reading, folks!

-- JC