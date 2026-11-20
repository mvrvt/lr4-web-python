from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from db import SessionLocal
from models import Product, User


def read_state():
    with SessionLocal() as session:
        balance = session.scalar(
            select(User.balance).where(User.id == 1)
        )
        stock = session.scalar(
            select(Product.stock).where(Product.id == 1)
        )
        return balance, stock


def prove_rejection(statement, constraint_name):
    before = read_state()

    try:
        with SessionLocal.begin() as session:
            result = session.execute(statement)

            if result.rowcount != 1:
                raise RuntimeError(
                    "Проверяемая строка не найдена. Подготовьте данные."
                )

    except IntegrityError as error:
        if (
            error.orig.pgcode != "23514"
            or error.orig.diag.constraint_name != constraint_name
        ):
            raise

    else:
        raise AssertionError(
            f"БД не отклонила нарушение {constraint_name}"
        )

    after = read_state()

    if after != before:
        raise AssertionError(
            f"Данные изменились: до={before}, после={after}"
        )

    print(
        f"{constraint_name}: операция отклонена, "
        f"данные сохранены: {after}"
    )


def main():
    prove_rejection(
        update(User)
        .where(User.id == 1)
        .values(balance=User.balance - 100000),
        "ck_users_balance_nonnegative",
    )

    prove_rejection(
        update(Product)
        .where(Product.id == 1)
        .values(stock=Product.stock - 100000),
        "ck_products_stock_nonnegative",
    )


if __name__ == "__main__":
    main()
