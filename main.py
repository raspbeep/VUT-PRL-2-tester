import os
import random
import subprocess

EXECUTABLE='../gol'

N_TESTS = 3     #number of test cases
MAX_LENGTH = 10 #width of the field
MAX_COUNT = 10  #height of the field
MIN_PROC = 0    #minimum number of processes
MAX_PROC = 10   #maximum number of processes
MIN_IT = 0      #minimum number of iterations
MAX_IT = 15     #maximum number of iterations

def read_field(filename):
    with open(filename, 'r') as f:
        field = []
        for row in f.read().splitlines():
            field.append([int(cell) for cell in row.strip()])
    return field

def count_neighbors(field, x, y):
    neighbors = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(field) and 0 <= ny < len(field[0]):
                neighbors += field[nx][ny]
    return neighbors

def next_state(current_field):
    next_field = []
    neighbors_field = []
    for x in range(len(current_field)):
        next_row = []
        for y in range(len(current_field[0])):
            neighbors = count_neighbors(current_field, x, y)
            neighbors_field.append(neighbors)
            if current_field[x][y] == 1 and neighbors in [2, 3]:
                next_row.append(1)
            elif current_field[x][y] == 0 and neighbors == 3:
                next_row.append(1)
            else:
                next_row.append(0)
        next_field.append(next_row)
    return next_field

def print_field(field):
    for row in field:
        print(''.join(map(str, row)))

def iterate(field, n_iters):
    f = field
    for i in range(n_iters):
        f = next_state(f)
    return f

def save_test_case(idx, testcase, name="input"):
    directory = f"tests/case_{idx}/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f"{directory}/{name}.txt", 'w') as f:
        for line in testcase:
            f.write(''.join(str(x) for x in line))
            f.write('\n')

def generate(n, max_length=MAX_LENGTH, max_count=MAX_COUNT):
    tests = []
    for i in range(n):
        test_case = []
        # only even numbers
        length = random.randint(1, max_length // 2) * 2
        count = random.randint(1, max_count // 2) * 2

        for c in range(count):
            line = []
            for l in range(length):
                line.append(random.choice((0, 1)))
            test_case.append(line)
        tests.append(test_case)

    return tests
            
def remove_tests(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                remove_tests(file_path)
        os.rmdir(directory)

def launch_executable(executable_path, np, it, case_idx):
    with open(f'./tests/case_{case_idx}/case_{case_idx}_np_{np}_it_{it}.out', 'w') as out_file, open(f'./tests/case_{case_idx}/case_{case_idx}_np_{np}_it_{it}.err', 'w') as err_file:
        subprocess.run(['mpirun', '--oversubscribe', '-np', str(np), executable_path, f'./tests/case_{case_idx}/input.txt', str(it)], stdout=out_file, stderr=err_file)

def compare_results(idx, np, it):
    with open(f'./tests/case_{idx}/differences', 'a') as diff_file:
        reference_path = f'./tests/case_{idx}/i_{it}.txt'
        test_path = f'./tests/case_{idx}/case_{idx}_np_{np}_it_{it}.out'
        command = f"bash -c 'diff <(sed \"s/[0-9]*: //\" {test_path}) {reference_path}'"
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            diff_file.write(f'test case idx:{idx} np:{np} it:{it}\n')
            print(f'Test case idx:{idx} np:{np} it:{it} failed')

if __name__ == '__main__':
    tests = generate(N_TESTS)

    remove_tests('./tests')

    for i in range(N_TESTS):
        save_test_case(i, tests[i])
        for l in range(MIN_IT, MAX_IT + 1):
            save_test_case(i, iterate(read_field(f'./tests/case_{i}/input.txt'), l), f'i_{l}')
        
        # test on multiple number of processes
        for np in range(MIN_PROC, MAX_PROC + 1):
            # test multiple iterations forward
            for l in range(MIN_IT, MAX_IT + 1):
                    launch_executable(EXECUTABLE, np, l, i)
                    compare_results(i, np, l)
