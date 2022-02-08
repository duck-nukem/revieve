from time import sleep

from reports import (
    generate_order_prices,
    generate_customer_ranking,
    generate_product_customers,
)

_HIDE_CURSOR = "\x1b[?25l"
_SHOW_CURSOR = "\x1b[?25h"
_PAUSE_SECONDS_BETWEEN_CHARS = 0.075


def typewrite(text: str) -> None:
    typed_word = ""

    for letter in text:
        typed_word += letter

        print(f"{typed_word}{_HIDE_CURSOR}\r", end="")
        sleep(_PAUSE_SECONDS_BETWEEN_CHARS)

    print(_SHOW_CURSOR)


def _clear():
    print("\033[H\033[J", end="")


if __name__ == "__main__":
    _clear()
    typewrite("Generating reports...")
    print("\n")

    report_generators = [
        generate_order_prices,
        generate_customer_ranking,
        generate_product_customers,
    ]

    for index, report_generator in enumerate(report_generators):
        report_generator()
        typewrite(f"Report {index + 1}/{len(report_generators)}...         done")

    print("\n")
    typewrite("Check the output folder for the generated reports. ✌️")
