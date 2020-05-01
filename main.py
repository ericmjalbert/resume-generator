from app.resume import Resume


def main():
    eric = Resume()
    print(eric.basics.name)
    print(eric.basics.location)
    print([job.company for job in eric.work])


if __name__ == "__main__":
    main()
