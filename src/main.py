#!/usr/bin/env python3

from app import App
import argparse

def main():
    parser = argparse.ArgumentParser(description="Nihao")
    parser.add_argument("--dataset", default="dataset/dataset", type=str, help="dataset folder")
    args = parser.parse_args()

    app = App()
    app.set_dataset(args.dataset)
    app.run()

if __name__ == "__main__":
    main()