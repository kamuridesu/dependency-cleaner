from depclean import main


if __name__ == "__main__":
    try:
        main.main()
    except KeyboardInterrupt:
        print("Operation cancelled!")
