import argparse
import csv
import numpy as np

from lib.utils import create_folders_for_path, p_array, brodatz_groups, kylberg_groups, load_image, brodatz_sample_count, kylberg_smaple_count
from lib.entropy import disp_en_2d, samp_en_2d, disp_samp_en_2d
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type=str, default='compute_entropy', help='compute_entropy, classification, compute_mean_std')
    parser.add_argument('--entropy', type=str, default='DispSampEn2D', help='DispEn2D, SampEn2D, DispSampEn2D')
    parser.add_argument('--m_array', type=int, nargs='+', default=[2, 3, 4], help='2, 3, 4, ...')
    parser.add_argument('--mapping', type=str, default='ncdf', help='ncdf, linear')
    parser.add_argument('--c', type=int, default=5, help='-1(for DispSampEn2D), 2, 3, ...')
    parser.add_argument('--r', type=float, default=0.24, help='0.24')
    parser.add_argument('--dataset', type=str, default='synthetic', help='synthetic, Brodatz, Kylberg')
    parser.add_argument('--p', type=str, default='0.0', help='0.0 ~ 1.0')
    parser.add_argument('--classifier', type=str, default='bayes', help='bayes, mlp')
    parser.add_argument('--rerun', default=False, action='store_true', help='rerun entropy computation or not')
    args = parser.parse_args()

    if args.task == 'compute_entropy':
        for m in args.m_array:
            compute_entropy(args.entropy, m, args.mapping, args.c, args.r, args.dataset, args.p)
    elif args.task == 'classification':
        if args.rerun:
            for m in args.m_array:
                compute_entropy(args.entropy, m, args.mapping, args.c, args.r, args.dataset, args.p)

        classification(args.entropy, args.m_array, args.dataset, args.p, args.classifier)
    elif args.task == 'compute_mean_std':
        if args.rerun:
            for m in args.m_array:
                compute_entropy(args.entropy, m, args.mapping, args.c, args.r, args.dataset, args.p)

        for m in args.m_array:
            compute_mean_std(args.entropy, m, args.dataset, args.p)
    else:
        print(f'Wrong task: {args.task}.')

def compute_entropy(entropy, m, mapping, c, r, dataset, p):
    if dataset == 'synthetic':
        output_path = f'output/{entropy}_{m}/synthetic.csv'
        print(f'Comput entropy, output path: {output_path}.')
        write_csv(output_path, ['p', 'entropy'], 'w+')

        for p_tmp in p_array:
            img = load_image(f'img/target/mix/{p_tmp}.jpg')
            output = entropy_helper(img, entropy, m, mapping, c, r)
            write_csv(output_path, [p_tmp, output], 'a+')
    else:
        output_path = f'output/{entropy}_{m}/{dataset}_{p}.csv'
        print(f'Comput entropy, output path: {output_path}.')
        write_csv(output_path, ['name', 'group', 'entropy'], 'w+')

        if dataset == 'Brodatz':
            groups = brodatz_groups
            count = brodatz_sample_count
        elif dataset == 'Kylberg':
            groups = kylberg_groups
            count = kylberg_smaple_count
        else:
            raise ValueError('No matching real-world dataset: {dataset}.')

        for group in groups:
            for index in range(1, count + 1):
                img = load_image(f'img/target/{dataset}/{group}_{index}_{p}.jpg')
                output = entropy_helper(img, entropy, m, mapping, c, r)
                write_csv(output_path, [f'{group}_{index}', group, output], 'a+')

def classification(entropy, m_array, dataset, p, classifier='bayes'):
    X, y = prepare_data(entropy, m_array, dataset, p)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1618)

    if classifier == 'bayes':
        classifier = GaussianNB()
    elif classifier == 'mlp':
        classifier = find_best_mlp_classifier(X_train, y_train)
    else:
        raise ValueError('No matching classifier.')

    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'[Accuracy: {accuracy}]')

def write_csv(path, row, mode):
    create_folders_for_path(path)
    with open(path, mode, newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

def entropy_helper(img, entropy = 'DispSampEn2D', m = 2, mapping = 'ncdf', c = -1, r = 0.24):
    if entropy == 'DispEn2D':
        return disp_en_2d(img, (m, m), mapping, c)
    elif entropy == 'SampEn2D':
        return samp_en_2d(img, (m, m), r)
    elif entropy == 'DispSampEn2D':
        return disp_samp_en_2d(img, (m, m), mapping, c)
    else:
        raise ValueError('No matching entropy algorithm: {entropy}.')

def prepare_data(entropy, m_array, dataset, p):
    print(f'Prepare data, entropy: {entropy}, m_array: {m_array}, dataset: {dataset}, p: {p}.')

    X = []
    y = []
    for m in m_array:
        count = 0
        input_path = f'output/{entropy}_{m}/{dataset}_{p}.csv'
        with open(input_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if len(X) <= count:
                    X.append([])
                    y.append(row['group'])
                if row['entropy'] == 'nan' or row['entropy'] == 'inf':
                    X[count].append(-1)
                else:
                    X[count].append(float(row['entropy']))
                count += 1
    return X, y

def find_best_mlp_classifier(X_train, y_train):
    # Can set the grid parameters here
    max_iter = 2000
    param_grid = {
        'hidden_layer_sizes': [(25, 25, 25, 25), (50, 50), (100,)],
        'activation': ['relu'],
        'solver': ['adam'],
        'alpha': [0.001],
    }

    mlp = MLPClassifier(max_iter=max_iter)
    grid_search = GridSearchCV(estimator=mlp, param_grid=param_grid, cv=5)
    grid_search.fit(X_train, y_train)
    print(f'Best parameters for MLP: {grid_search.best_params_}.')
    return grid_search.best_estimator_

def compute_mean_std(entropy, m, dataset, p):
    print(f'Compute mean and std by groups for entropy: {entropy}, m: {m}, dataset: {dataset}, p: {p}.')

    if dataset == 'Brodatz':
        groups = brodatz_groups
    elif dataset == 'Kylberg':
        groups = kylberg_groups
    else:
        raise ValueError('No matching real-world dataset: {dataset}.')

    # Initialize the dictionary
    entropy_lists_by_groups = {}
    for group in groups:
        entropy_lists_by_groups[group] = []

    input_path = f'output/{entropy}_{m}/{dataset}_{p}.csv'
    with open(input_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['entropy'] != 'nan' and row['entropy'] != 'inf':
                entropy_lists_by_groups[row['group']].append(float(row['entropy']))

    for group, entropy_list in entropy_lists_by_groups.items():
        print(f'Group: {group}, mean: {np.average(entropy_list)}, std: {np.std(entropy_list)}.')

if __name__ == '__main__':
    main()