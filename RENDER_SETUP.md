# Render setup (petpal-server)

## 1. Web service → Settings → Build & Deploy

**Build Command:**

```bash
pip install -r requirements-prod.txt
```

**Start Command:**

```bash
cd petpal && python manage.py migrate && python manage.py seed_pets_if_empty && gunicorn petpal.wsgi:application
```

Click **Save Changes** (Render redeploys automatically).

## 2. Web service → Environment

Link your Postgres database (or add `DATABASE_URL` from the database’s **Internal** connection string).

Without `DATABASE_URL`, the app uses SQLite and data can wipe on redeploy.

## 3. After deploy

1. Sign up or **Reset password** on the live site.
2. Log in — pets should persist across future deploys.
