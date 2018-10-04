import click
from apt2b.core import process_csv


@click.command()
@click.argument("filename")
def run_script(filename):
    process_csv(filename)


if __name__ == "__main__":
    process_csv("Apt2B - CJ - Aug 28.csv")
