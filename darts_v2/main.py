from darts_v2 import App


def main():
    app = App()

    app.geometry('800x600')

    app.run(fps=1)


if __name__ == '__main__':
    main()
