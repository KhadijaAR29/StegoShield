"""
main.py  --  OWNER: Khadija
Command-line entry point (also handy for quick testing before the GUI exists).

Usage:
    python main.py embed   cover.png out.png "secret text" password [--mode random|sequential]
    python main.py extract out.png password [--mode random|sequential]
    python main.py detect  image.png
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="StegoShield")
    sub = parser.add_subparsers(dest="command", required=True)

    e = sub.add_parser("embed")
    e.add_argument("cover")
    e.add_argument("out")
    e.add_argument("message")
    e.add_argument("password")
    e.add_argument("--mode", default="random", choices=["random", "sequential"])

    x = sub.add_parser("extract")
    x.add_argument("stego")
    x.add_argument("password")
    x.add_argument("--mode", default="random", choices=["random", "sequential"])

    d = sub.add_parser("detect")
    d.add_argument("image")

    args = parser.parse_args()

    if args.command == "embed":
        from stego.embed import embed_message
        print(embed_message(args.cover, args.out, args.message, args.password, args.mode))
    elif args.command == "extract":
        from stego.extract import extract_message
        try:
            print(extract_message(args.stego, args.password, args.mode))
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == "detect":
        from analysis.detector import detect
        print(detect(args.image))


if __name__ == "__main__":
    main()
