# demo-user-reviews
A sample project analyzing user reviews and ratings


# Setup

Run `pip install -r requirements`.

Obtain a `client id` and an `api key` by [creating a Yelp app](https://www.yelp.com/developers/v3/manage_app) and update the following variables in the `.env` file.

```
YELP_CLIENT_ID
YELP_API_KEY
```

## Setup Database
Change directories to `/app/db` and run `docker compose up`.

Update values in `.env` and make sure the postgres vals match whatever was entered in `/app/db/.env`.

