import shutil
import subprocess
import pandas
import os.path
import time


def run_one_dim(dim, name=None, num_runs=20):
    ''' Run for one setting '''
    settings_file_name = 'settings_{}.py'.format(name)
    data_file_name = '{}/{}_connectivity_result.dat'.format(name, dim)
    out_file_name = 'output/{}_{}_all.csv'.format(name, dim)
    cmd_run = 'python exp.py {} -d {}'.format(dim, name)

    # mkdirs
    work_dir = './{}'.format(name)
    if not os.path.exists(work_dir):
        os.mkdir(work_dir)
    if not os.path.exists('./output'):
        os.mkdir('./output')

    # copy settings
    shutil.copyfile(settings_file_name, 'settings.py')

    df = pandas.DataFrame()
    for run_id in range(num_runs):
        start = time.time()
        print('Running {}({}) {}/{}'.format(name, dim, run_id+1, num_runs))
        # run exp
        process = subprocess.Popen(cmd_run.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        # analyze result
        with open(data_file_name, 'r') as data:
            lines = data.readlines()

        rows = []
        for line in lines:
            if line:
                time_step, connectivity = line.split()
                rows.append( [int(time_step), float(connectivity)] )
        df_each_run = pandas.DataFrame(rows, columns=['time run={}'.format(run_id), 'Connectivity run={}'.format(run_id)])
        df[df_each_run.columns] = df_each_run
        end = time.time()
        print('Running {}({}) {}/{} took {:.1f} seconds'.format(name, dim, run_id+1, num_runs, end-start))
    df.to_csv(out_file_name)


def run():
    dimensions = [6, 2, 4, 6, 8, ]
    names = ['control', 2, 4, 6, 8]
    num_runs = [20] * 5

    for dim, name, num_run in zip(dimensions, names, num_runs):
        run_one_dim(dim, name, num_run)


if __name__ == '__main__':
    run()
