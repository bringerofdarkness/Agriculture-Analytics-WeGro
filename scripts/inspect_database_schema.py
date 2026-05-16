from sqlalchemy import text

from app.database import get_connection


def print_section(title: str) -> None:
    print()
    print("=" * 90)
    print(title)
    print("=" * 90)


def main() -> None:
    with get_connection() as connection:
        print_section("DATABASE")
        database_name = connection.execute(text("SELECT DATABASE()")).scalar_one()
        print(database_name)

        print_section("TABLES AND VIEWS")
        tables = connection.execute(
            text(
                """
                SELECT
                    TABLE_NAME AS table_name,
                    TABLE_TYPE AS table_type,
                    ENGINE AS engine,
                    TABLE_ROWS AS table_rows
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                ORDER BY TABLE_TYPE, TABLE_NAME
                """
            )
        ).mappings().all()

        for row in tables:
            print(dict(row))

        print_section("COLUMNS")
        columns = connection.execute(
            text(
                """
                SELECT
                    TABLE_NAME AS table_name,
                    COLUMN_NAME AS column_name,
                    DATA_TYPE AS data_type,
                    IS_NULLABLE AS is_nullable,
                    COLUMN_KEY AS column_key,
                    COLUMN_DEFAULT AS column_default
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                ORDER BY TABLE_NAME, ORDINAL_POSITION
                """
            )
        ).mappings().all()

        current_table = None

        for row in columns:
            table_name = row["table_name"]

            if table_name != current_table:
                current_table = table_name
                print()
                print(f"[{current_table}]")

            print(
                f"  - {row['column_name']} "
                f"({row['data_type']}, nullable={row['is_nullable']}, key={row['column_key']})"
            )

        print_section("VIEW DEFINITIONS")
        views = connection.execute(
            text(
                """
                SELECT
                    TABLE_NAME AS table_name,
                    VIEW_DEFINITION AS view_definition
                FROM information_schema.VIEWS
                WHERE TABLE_SCHEMA = DATABASE()
                ORDER BY TABLE_NAME
                """
            )
        ).mappings().all()

        for view in views:
            print()
            print(f"[{view['table_name']}]")
            print(view["view_definition"])


if __name__ == "__main__":
    main()