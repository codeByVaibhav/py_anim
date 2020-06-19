import subprocess
def parallel_command(commands, n_threads=8):
    '''
    Takes list of console commands and exucute them in parallel
    '''
    run = True
    running = []
    while len(commands) > 0:
        if len(running) < n_threads and run:
            running.append(subprocess.Popen(commands.pop(0), subprocess.PIPE))
        running = [r for r in running if r.poll() is None]
        run = False if len(running) >= n_threads else True