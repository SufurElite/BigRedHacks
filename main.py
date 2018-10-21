import stats, machineLearning, os, sys


def main():
    if len(sys.argv)>1:
        file_path = sys.argv[1].replace("[", " ").replace("]", "\\")
        path_name = sys.argv[2].replace("[", " ").replace("]", "\\")
        machineLearning.predict(file_path, path_name)
        return None;
    stats.createStats(True);
    #machineLearning.graph(True);
    machineLearning.trainModel(False);

    return None;

main();
