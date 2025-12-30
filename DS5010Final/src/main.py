from pipeline import Pipeline
import config

def main():
    '''
    Pipeline is an object from the Piepline class, where attributes are

    set to config paths. See config.py for these csv paths.

    This main() needs to run Pipeline's main as matrix is built and 

    dendrogram is plotted given features from each csv path
    '''
    pipeline = Pipeline(
        config.FMR_PATH,
        config.WAGE_PATH,
        config.INCOME_PATH
    )
    pipeline.main()

if __name__ == "__main__":
    main()
