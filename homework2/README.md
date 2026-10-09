# Movie Theater Booking (Homework 2)

A Django web app and REST API for browsing movies, picking seats and managing bookings.

**Live app:** https://cs4300-991r.onrender.com/

## Features
- Movie listings, seat selection and booking history pages (Django templates + Bootstrap 5)
- REST API built with Django REST Framework viewsets
- Login/logout with Django's built-in auth; users only see their own bookings
- Double-booking protection: a seat can be booked once **per movie** (the same seat can be booked for a different movie), enforced in the database and in code
- Unit, integration and BDD (Behave) tests

## Project structure
```
homework2/
├── manage.py
├── requirements.txt          # Python dependencies
├── build.sh                  # Render build script
├── movie_theater_booking/    # project config (settings, urls, wsgi)
├── bookings/                 # the app
│   ├── models.py             # Movie, Seat, Booking
│   ├── serializers.py        # JSON serializers
│   ├── views.py              # DRF viewsets + HTML views
│   ├── services.py           # booking / cancelling logic shared by API and pages
│   ├── urls.py               # page routes + API router
│   ├── admin.py
│   ├── tests.py              # unit + integration tests
│   ├── templates/            # bookings/*.html, registration/login.html
│   └── management/commands/seed_demo.py   # creates demo seats and movies
└── features/                 # Behave (BDD)
    ├── booking.feature
    └── steps/booking_steps.py
```

## Setup
```bash
cd homework2
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo          # optional: 20 seats and 3 movies
python manage.py createsuperuser    # admin account for /admin/
```

## Run locally (DevEdu)
```bash
python3 manage.py runserver 0.0.0.0:3000
```
Then open the **app** button in the DevEdu dashboard. The DevEdu URL must be listed in
`CSRF_TRUSTED_ORIGINS` and `ALLOWED_HOSTS` in `settings.py` for login to work.

## Pages and API
| URL | What it does |
|---|---|
| `/` | Movie listings |
| `/movies/<id>/book/` | Pick and book a seat (login required) |
| `/my-bookings/` | Booking history, with cancel buttons (login required) |
| `/accounts/login/` | Log in |
| `/admin/` | Admin site (add movies and seats) |
| `/api/movies/` | List movies; full CRUD (writes are admin only) |
| `/api/seats/` | Seat availability. `?movie=<id>` shows status for that movie, `?status=available` filters; `POST /api/seats/<id>/book/` with `{"movie": <id>}` |
| `/api/bookings/` | Your booking history; `POST {"movie": <id>, "seat": <id>}` to book; `DELETE /api/bookings/<id>/` to cancel |

## Tests
```bash
python manage.py test bookings      # unit + integration tests
python manage.py behave             # BDD scenarios (features/booking.feature)

# optional: coverage
pip install coverage
coverage run --source=bookings manage.py test bookings
coverage report --omit="bookings/migrations/*"
```

## Deployment (Render)
The app is deployed as a Render Web Service from this repository.

| Setting | Value |
|---|---|
| Root Directory | `homework2` |
| Build Command | `bash build.sh` |
| Start Command | `gunicorn movie_theater_booking.wsgi:application` |
| Environment | `DEBUG=False`, `SECRET_KEY`, `PYTHON_VERSION=3.12.3`, `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`, `DJANGO_SUPERUSER_EMAIL` |

`build.sh` installs dependencies, collects static files, runs migrations, seeds demo data and
creates the admin account. Note: the default SQLite database is reset on each deploy on
Render's free tier; set `DATABASE_URL` to a Render Postgres database for persistent data.

## AI use
- **Tool:** Claude (Anthropic), via the Claude chat interface.
- **What it helped with:** drafting the initial models, serializers, DRF viewsets, URL routing,
  HTML templates, unit/integration tests and Behave scenarios; the Render deployment files
  (`build.sh`, `requirements.txt`, production settings and the `seed_demo` command); the Bootstrap
  styling; and diagnosing errors (git push authentication, template paths, CSRF origin, Render build logs).
- **How the results were used:** the generated code was copied into the project, adapted to my
  project layout and names, and run and tested locally and in DevEdu before being committed.
  I fixed file placement problems and verified the test suites pass myself.