from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError

from app.database import get_connection


def main() -> None:
    """
    Verify MySQL connectivity and confirm that the main PRD view is accessible.
    """
    try:
        with get_connection() as connection:
            database_name = connection.execute(text("SELECT DATABASE()")).scalar_one()

            harvest_view_count = connection.execute(
                text("SELECT COUNT(*) FROM vw_harvest_full")
            ).scalar_one()

            print(f"Connected to database: {database_name}")
            print(f"vw_harvest_full rows: {harvest_view_count}")

    except OperationalError as exc:
        print("Database operational error.")
        print("Check host, port, username, password, network access, or DB permissions.")
        print(f"Details: {exc}")
        raise SystemExit(1) from exc

    except ProgrammingError as exc:
        print("Database SQL/programming error.")
        print("Check whether vw_harvest_full exists and is accessible to this user.")
        print(f"Details: {exc}")
        raise SystemExit(1) from exc

    except SQLAlchemyError as exc:
        print("General SQLAlchemy database error.")
        print(f"Details: {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()